We use with open(...) because it automatically closes the file when the block finishes. It also closes the file if an exception occurs, making the code safer and preventing resource leaks. We don't need to manually call close().

TypeError occurs when an operation or function receives an inappropriate type. ValueError occurs when the type is appropriate but the value is invalid or unacceptable.