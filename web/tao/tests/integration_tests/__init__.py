from .mock_galaxy_factory import MockGalaxyFactoryTest
from .jobs import JobTest

ALL_INTEGRATION_TEST_CASES = (
    JobTest,
    MockGalaxyFactoryTest,
)
