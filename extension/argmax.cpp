#include <torch/extension.h>


int64_t argmax(torch::Tensor y) {
  return torch::argmax(y).item().toInt();

}


PYBIND11_MODULE(TORCH_EXTENSION_NAME, m) {
  m.def("argmax", &argmax, "Argmax");
}

