from django.test.testcases import TestCase

from tao.pagination import paginate


class PaginationTest(TestCase):
    def testPaginationBasic(self):
        nums = [x for x in range(10)]
        paginated = paginate(nums, 1, per_page=3)
        self.assertEquals([0, 1, 2], paginated.object_list)

    def testPaginationNonInteger(self):
        nums = [x for x in range(10)]
        paginated = paginate(nums, 'a', per_page=3)
        self.assertEquals([0, 1, 2], paginated.object_list)

    def testPaginationNonInteger(self):
        nums = [x for x in range(10)]
        paginated = paginate(nums, '999', per_page=3)
        self.assertEquals([9], paginated.object_list)
