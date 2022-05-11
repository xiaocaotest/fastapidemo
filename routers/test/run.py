import os
import unittest

from BSTestRunner import BSTestRunner


def suite():
    import os
    path = os.getcwd()
    suite = unittest.TestLoader().discover(path, pattern='test*.py', top_level_dir=None)
    return suite


if __name__ == "__main__":
    BASH_DIR = "history"
    report_path = os.path.join(BASH_DIR, "test.html")
    openone = open(report_path, 'w+')
    besautiful = BSTestRunner(title="报告",
                              description="测试报告",
                              stream=openone,
                              trynum=2,
                              filepath=BASH_DIR,
                              is_show=True)
    all = suite()
    besautiful.run(all)
