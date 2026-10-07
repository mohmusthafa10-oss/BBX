Weather CLI — Answers
Failure Tests
Wrong API key
Status: 401 Unauthorized
Invalid city
Status: 404 Not Found
timeout=0.001
Exception: requests.exceptions.Timeout
1. Which HTTP methods are safe to retry, and why?
GET, HEAD, OPTIONS, and TRACE are generally safe to retry because they are designed to retrieve or inspect data without changing server state. PUT and DELETE are idempotent, so repeating the same request should produce the same final state. This matters because network failures can occur even after a server receives a request. Retrying a non-idempotent operation such as POST could accidentally create duplicate data or actions. Therefore, understanding which methods can safely be retried helps prevent unintended side effects.
2. What is the difference between 401 and 403?
401 Unauthorized means authentication is missing or invalid. For example, an API key may be wrong or expired. The client needs valid credentials. 403 Forbidden means the server understands the client but refuses access because the client does not have permission. In simple terms: 401 = authentication problem; 403 = permission problem.
3. Why must you always set a timeout?
A timeout prevents a program from waiting indefinitely for a network response. Servers can become slow, unavailable, or unreachable. Without a timeout, the application may appear frozen. With a timeout, the program can catch requests.exceptions.Timeout, show a useful message, and continue or exit gracefully. Timeouts therefore improve reliability, responsiveness, and user experience.