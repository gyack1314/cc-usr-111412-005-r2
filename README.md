# 企业调用用途的组成变化与总量分离监测

项目提供智能消费业务分析使用的来源准备接口。记录为合成资料，不对应真实平台客户。counts.py只区分结构不可用、缺测、真零并给完整周的直接比例。未做零值建模、变化点估计或误报校准。

`taxonomy.py`、`counts.py`负责实际资料语义，`analytics.py`调用这些接口形成当前可用输入。`common.py`提供精确金额、时点修订读取和摘要绑定的不可变发布。来源字段与语义见[资料契约](docs/contracts.md)。

运行环境为Python 3.11，当前依赖仅标准库。以下命令在项目根目录执行：

```sh
python -m unittest discover -s tests -v
python -m compileall -q .
python -m analytics
```

Linux环境也可执行：

```sh
docker build -t intelligent-consumption .
docker run --rm --network=none intelligent-consumption
docker run --rm --network=none intelligent-consumption python -m analytics
```

运行创建的报告和临时文件使用`.runtime/`，不将本机账号配置写入项目。
