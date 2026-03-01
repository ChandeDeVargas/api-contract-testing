"""
Breaking Change Detection Tests
Tests the BreakingChangeDetector by comparing two versions of the Users API
"""
import pytest
from pathlib import Path
from tests.utils.breaking_change_detector import BreakingChangeDetector

class TestBreakingChangeDetection:
    """
    Validate that breaking changes are correctly detected between API versions.
    """
    
    @pytest.fixture
    def v1_spec_path(self):
        """Path to v1 (old) OpenAPI spec"""
        return "contracts/openapi-specs/users-api-v1.yaml"
    
    @pytest.fixture
    def v2_spec_path(self):
        """Path to v2 (new) OpenAPI spec"""
        return "contracts/openapi-specs/users-api-v2.yaml"
    
    @pytest.fixture
    def detector(self, v1_spec_path, v2_spec_path):
        """Initialize detector with v1 and v2 specs"""
        return BreakingChangeDetector(v1_spec_path, v2_spec_path)

    def test_detector_initialization(self, detector):
        """Test: Detector initializes correctly with both specs"""
        assert detector.old_spec is not None
        assert detector.new_spec is not None
        assert detector.old_spec['info']['version'] == '1.0.0'
        assert detector.new_spec['info']['version'] == '2.0.0'
        print("\nDetector: Initialized successfully with v1 and v2")

    def test_detect_all_breaking_changes(self, detector):
        """
        Test: All breaking changes are detected
        
        This test ensures that the detector finds changes between v1 and v2.
        """
        changes = detector.detect_all_changes()
        summary = detector.get_summary(changes)
        
        print(f"\nBreaking Changes Found: {summary['total']}")
        print(f"Critical Changes: {summary['critical_count']}")
        
        # In this specific project, v1 -> v2 should have breaking changes
        assert summary['total'] > 0, "No breaking changes detected between v1 and v2"
        
        # Log detected changes for visibility
        for change in changes:
            print(f"  - [{change.severity.upper()}] {change.category}: {change.description} at {change.path}")

    def test_specific_breaking_changes(self, detector):
        """
        Test: Specific types of breaking changes are detected
        """
        changes = detector.detect_all_changes()
        categories = [c.category for c in changes]
        
        # Check for expected categories of changes between v1 and v2
        # (Based on common breaking change scenarios)
        assert any(cat in categories for cat in ['field_removed', 'type_changed', 'endpoint_removed', 'response_code_changed']), \
            "Expected common breaking change categories not found"

    def test_critical_changes_impact(self, detector):
        """
        Test: Critical changes have impact descriptions
        """
        changes = detector.detect_all_changes()
        critical_changes = [c for c in changes if c.severity == 'critical']
        
        for change in critical_changes:
            assert change.impact != "", f"Critical change {change.category} missing impact description"
            impact_lower = change.impact.lower()
            assert any(word in impact_lower for word in ["break", "fail", "error"]), \
                f"Impact description for {change.category} should mention breakage or errors: '{change.impact}'"

    def test_no_changes_same_file(self, v1_spec_path):
        """
        Test: No changes detected when comparing same file
        """
        detector_same = BreakingChangeDetector(v1_spec_path, v1_spec_path)
        changes = detector_same.detect_all_changes()
        
        assert len(changes) == 0, "Breaking changes detected when comparing identical specs"
        print("\nRegression Check: No changes detected for identical specs")