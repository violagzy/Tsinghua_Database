# -*- coding:utf-8 -*-

"""本程序的主要目的是分析看视频情况与最后课程得分的关联"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl


def conf_zh():
    """初始化中文字体"""
    mpl.rcParams['font.sans-serif'] = ["simhei"]
    mpl.rcParams['axes.unicode_minus'] = False


class Project:

    def read_data(self, path1e, path1g, path2e, path2g, path3e, path3g):
        """读取csv格式数据，数字1/2/3分别对应清华学生、外校学生、所有学生，字母e、g、v分别对应选课（enroll）/成绩（grade）"""
        self.df1e = pd.read_csv(path1e)
        self.df1g = pd.read_csv(path1g)
        self.df2e = pd.read_csv(path2e)
        self.df2g = pd.read_csv(path2g)
        self.df3e = pd.read_csv(path3e)
        self.df3g = pd.read_csv(path3g)


    def pre(self):
        """进行表拼接和数据类型转换"""

        """将e/g两张表根据多键进行拼接"""
        self.df1 = pd.merge(self.df1e, self.df1g, on=['学堂号', '姓名', '昵称', '学号', '学院', '成绩', '课程得分', '课程得分率'], how='inner')
        self.df2 = pd.merge(self.df2e, self.df2g, on=['学堂号', '姓名', '昵称', '成绩', '课程得分', '课程得分率'], how='inner')
        self.df3 = pd.merge(self.df3e, self.df3g, on=['学堂号', '昵称', '成绩', '课程得分', '课程得分率'], how='inner')

        """数据类型转换"""
        def transform(self, df):
            attributes = ['理论考试的得分率', '课程学习比例', '课程得分率', '习题作业的得分率']
            for a in attributes:
                df[a] = df[a].str.replace('%', '')
                df[a] = df[a].astype('float64')

        for self.df in [self.df1, self.df2, self.df3]:
            transform(self, self.df)

    def filter_data(self):
        """初步过滤数据，滤除僵尸用户"""

        self.df1_active = self.df1[
            (self.df1['选课状态'] == '选课中') &
            (self.df1['理论考试的得分率'] > 0) &
            (self.df1['习题作业的得分率'] > 0)
            ]

        self.df2_active = self.df2[
            (self.df2['选课状态'] == '选课中') &
            (self.df2['理论考试的得分率'] > 0) &
            (self.df2['习题作业的得分率'] > 0)
            ]

        self.df3_active = self.df3[
            (self.df3['选课状态'] == '选课中') &
            (self.df3['理论考试的得分率'] > 0) &
            (self.df3['习题作业的得分率'] > 0)
            ]

    def visualize_horizontal(self):
        """横向对比三类学生成绩"""
        def visualize_grade(self, df1, df2, df3):
            """对比三类学生的课程得分率"""
            sns.set(style="white", palette="muted", color_codes=True)
            conf_zh()

            sns.distplot(df1['课程得分率'], hist=False, color="plum", kde_kws={"shade": True}, kde=True)
            plt.ylim(0, 0.10)
            plt.xlim(0, 100)

            sns.distplot(df2['课程得分率'], hist=False, color="lightgreen", kde_kws={"shade": True}, kde=True)
            plt.ylim(0, 0.10)
            plt.xlim(0, 100)

            sns.distplot(df3['课程得分率'], hist=False, color="cornflowerblue", kde_kws={"shade": True}, kde=True)
            plt.ylim(0, 0.10)
            plt.xlim(0, 100)


            plt.show()

        for [df1, df2, df3] in [[self.df1, self.df2, self.df3], [self.df1_active, self.df2_active, self.df3_active]]:
            visualize_grade(self, df1, df2, df3)

    def visualize_vertical(self):
        """纵向对比课程得分率、课程学习比例、习题作业的得分率、理论考试的得分率分布情况"""
        def vertical(self, df):
            sns.set(style="white")
            conf_zh()
            numerical = df.loc[:, ['课程得分率', '课程学习比例', '习题作业的得分率', '理论考试的得分率']]
            sns.boxplot(data=numerical, palette="muted")
            plt.ylim(0, 101)
            plt.show()
        for df in [self.df1_active, self.df2_active, self.df3_active]:
            vertical(self, df)

    def pair_grade_video(self):
        def p_grade_video(self, df0):
            """分析视频观看情况和分数之间的分布关系"""
            sns.set(style="white")
            conf_zh()
            add = pd.DataFrame(df0, columns=['课程得分率', '课程学习比例', '课程得分比'])
            add['课程得分比'] = df0['课程学习比例']/df0['课程得分率']-1
            sns.lmplot(x="课程得分率", y="课程得分比", data=add)
            plt.xlim(0, 100)
            plt.ylim(-1, 0.6)
            plt.axvline(x=60, color="r", linestyle="--")
            plt.axvline(x=90, color="b", linestyle="--")
            plt.axvline(x=100, color="y", linestyle="--")
            plt.axhline(y=0, xmin=0, xmax=1, color="g", linestyle=":")
            plt.show()
        for df in [self.df1_active, self.df2_active, self.df3_active]:
            p_grade_video(self, df)

    def regression_grade_video(self):
        def reg_grade_video(self, df0):
            """分析视频观看情况和分数之间的相关关系"""
            sns.set(style="white")
            conf_zh()
            sns.jointplot(x="课程学习比例", y="课程得分率", kind="hex", data=df0)
            plt.show()
        for df in [self.df1_active, self.df2_active, self.df3_active]:
            reg_grade_video(self, df)

    def student(self):
        """分析不同学生类型"""
        sns.set(style="white")
        conf_zh()
        add = pd.DataFrame(self.df3_active, columns=['课程得分率', '课程学习比例', '课程得分比'])
        add['课程得分比'] = self.df3_active['课程学习比例']/self.df3_active['课程得分率']-1
        sns.lmplot(x="课程得分率", y="课程得分比", data=add)
        plt.xlim(0, 100)
        plt.ylim(-1, 0.6)
        plt.axvline(x=60, color="r", linestyle="--")
        plt.axvline(x=90, color="b", linestyle="--")
        plt.axvline(x=100, color="y", linestyle="--")
        plt.axhline(y=0, xmin=0, xmax=1, color="g", linestyle=":")
        plt.text(25, -0.5, '学渣', fontsize=20, color="r")
        plt.text(25, 0.3, '学弱', fontsize=20, color="r")
        plt.text(70, -0.5, '学痞', fontsize=20, color="b")
        plt.text(70, 0.3, '学民', fontsize=20, color="b")
        plt.text(90, -0.5, '学霸', fontsize=20, color="y")
        plt.text(90, 0.3, '学神', fontsize=20, color="y")
        plt.show()


p = Project()
p.read_data('course-v1-TsinghuaX+20740042X+2016-T2_enroll (1).csv',
            'course-v1-TsinghuaX+20740042X+2016-T2_grade (1).csv',
            'course-v1-TsinghuaX+20740042X+2016-T2_enroll (2).csv',
            'course-v1-TsinghuaX+20740042X+2016-T2_grade (2).csv',
            'course-v1-TsinghuaX+20740042X+2016-T2_enroll.csv',
            'course-v1-TsinghuaX+20740042X+2016-T2_grade.csv')
p.pre()
p.filter_data()
# p.visualize_horizontal()
# p.visualize_vertical()
# p.regression_grade_video()
# p.pair_grade_video()
# p.student()
