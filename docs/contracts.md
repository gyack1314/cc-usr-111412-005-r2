# 来源接口与业务口径

taxonomy.py的mapping验证显式多对一类别映射，reclassify返回改类明细和unmapped明细，不自动猜测版本语义；多对一后的聚合由调用方处理。

counts.py的panels按org/week/category校验唯一性。available=false表示结构不可用，observed=false表示缺测，observed=true且count=0表示真零。完整可用面板返回total和proportions；缺测时total为null，零总量时proportions为null。分类计数是互斥事件数。当前摘要不包含变化检测或报警阈值。

输入为UTF-8 JSON，金额为十进制字符串。样例是合成资料，不限定分析数据规模。
