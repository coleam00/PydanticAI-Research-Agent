Okay, there's actually a problem with my codebase. When I interact with the agent through the actual application and it uses the search tool, it fails. But all my unit tests pass, so they're not catching this real-world issue.

I need help evolving my validate.md so it catches real runtime problems. Not just for the research agent but the entire agent application. Here's what I'm thinking: instead of just running predefined test scripts, what if we had a way for you (the AI assistant) to actually interact with the agent like a real user would? You could design test scenarios on the fly based on what you think might break.

The key thing is: I don't want static, predefined tests. Nothing like using pytest. I want you to be able to interact with the agent through a CLI and intelligently decide what to test in real-time. Think about how a user would actually run the agent from the command line.

Help me design this approach. What would we need to build to make this work?