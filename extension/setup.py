from setuptools import setup, Extension
from torch.utils import cpp_extension

setup(
    name="argmax_cpp",
    ext_modules=[cpp_extension.CppExtension("argmax_cpp", ["argmax.cpp"])],
    cmdclass={"build_ext": cpp_extension.BuildExtension},
)

Extension(
    name="argmax_cpp",
    sources=["argmax.cpp"],
    include_dirs=cpp_extension.include_paths(),
    language="c++",
)
