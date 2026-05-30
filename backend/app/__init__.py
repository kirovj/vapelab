"""FastAPI 应用后端"""
import typing


def _patch_sqlmodel_annotations() -> None:
    """修复 sqlmodel 在 Python 3.14+ 下的兼容性问题。

    Python 3.14 改变了元类命名空间中注解的存储方式：
    - 旧版：class_dict 中包含 __annotations__ 键
    - 新版：class_dict 中包含 __annotate_func__() 可调用对象
    sqlmodel 0.0.22 未适配此变更，导致 get_annotations 返回空字典。
    需要同时修补 _compat 和 main 两个模块中导入的引用。
    """
    try:
        import sqlmodel._compat as compat
        import sqlmodel.main as main

        def _get_annotations(
            class_dict: dict[str, typing.Any],
        ) -> dict[str, typing.Any]:
            annotations = class_dict.get("__annotations__")
            if annotations is not None:
                return annotations
            annotate_func = class_dict.get("__annotate_func__")
            if annotate_func is not None:
                return annotate_func(0)
            return {}

        compat.get_annotations = _get_annotations
        main.get_annotations = _get_annotations
    except ImportError:
        pass


_patch_sqlmodel_annotations()
