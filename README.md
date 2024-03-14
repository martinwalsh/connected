# connected

## Experiments in Pipeline/Workflow syntax

This project is an exploration of Python syntax and recent language features,
intended to implement an inheritable base class for applications that require
sharing data across invocations and between objects, such as AI pipelines and
workflows. Its intention is primarily a personal learning exercise, but hopes to
find a novel solution to the problem through experimentation. It draws
inspiration from langchain's LCEL (LangChanin Expression Language). 

## Getting Started

To get started with this project, follow these steps:

- Clone the repository: git clone https://github.com/martinwalsh/connected.git
- Run `rye sync` (for more information on [rye](https://github.com/astral-sh/rye) check out the [rye documentation](https://rye-up.com/))
- Explore the code and experiment with the `Context` and `LazyRef` objects.
- Take a look in the [`tests`](./tests) directory for examples.
- Share your feedback and contribute to the project if you find it interesting!

## Resources

- [langchain's LCEL](https://python.langchain.com/docs/expression_language/): The inspiration behind this project

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for more information.