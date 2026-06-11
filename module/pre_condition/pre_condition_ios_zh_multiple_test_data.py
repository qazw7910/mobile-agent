import pytest

from module.mobile.cube_util import CubeUtil
from module.pre_condition.pre_condition_ios_zh import PreConditionIosZh


class PreConditionIosZhMultipleTestData(PreConditionIosZh):
    @pytest.fixture(autouse=True)
    def setup_test_data(self, request):
        """
        繼承PreConditionIosZh初始化方法 但額外處理多標題＋多測資的情境
        呼叫user資料時 需呼叫users而不是user
        """
        if hasattr(request, 'param'):
            self.title, self.user = request.param
            self.users = CubeUtil.ios_json_cube_user(self.user)
            self.navigator.cube.login(self.users)
        return
