# Contributing to RTSC

We welcome contributions to the Real-Time Suggestive Contour (RTSC) viewer!

## How to Contribute

1. **Report Bugs:** If you find a bug, please open an issue describing the problem, including the steps to reproduce it.
2. **Suggest Features:** Have an idea for a new feature? Open an issue to discuss it.
3. **Submit Pull Requests:** We accept pull requests. Please ensure your code follows the existing style and that it compiles and passes tests.

## Development Setup

```bash
git clone https://github.com/<your-fork>/SuggestiveContours.git
cd SuggestiveContours
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build . -j$(nproc)
```

## Coding Standards

- **C++20** standard
- Zero compiler warnings
- Use `constexpr` for compile-time constants
- Use `[[nodiscard]]` for functions that must not ignore return values
- Use `[[maybe_unused]]` for intentionally unused variables

## Submitting a Pull Request

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make changes ensuring zero warnings
3. Test locally: `cmake --build .`
4. Push and open a PR against `main`

CI runs:
- Build on Ubuntu/macOS with clang/gcc
- Code style check with clang-format

Thank you for contributing!
