# exargparse

## BaseHandler

当一个（子）解析器需要使用 `action` 选项执行不同的事务时，我们可以在 `BaseHandler` 的子类（**处理器**）中实现这些动作。使用 `@staticmethod` 装饰器将每个动作定义为类的静态方法（方法名与动作名相同），该方法只接受一个参数 `args`，代表解析器返回的参数对象（`Namespace` 实例）。参数解析完成后调用处理器的 `run()` 方法并传入解析的参数对象执行程序。

## SmartFormatter

作为 `formatter_class` 传入（子）解析器，允许为参数选项的 `help` 设置多行字符串。

## ExArgumentParser

继承自 `argparse` 提供的 `ArgumentParser` 类，做了一些简单的封装，主要内容有：
1. 使用 `SmartFormatter` 作为默认的消息格式化工具
2. 提供 `get_subparser` 方法快速创建子解析器对象
3. 提供 `set_callback` 方法设置（子）解析器的回调函数或者回调处理器
4. 提供 `run` 方法调用预设的回调工具执行程序

python setup.py sdist && pip install dist/exuse-0.1.3.tar.gz --force-reinstall

N=4 && python setup.py sdist && pip install dist/exuse-0.1.$N.tar.gz && twine upload dist/exuse-0.1.$N.tar.gz 