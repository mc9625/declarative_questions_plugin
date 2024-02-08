# declarative_questions_plugin
A plugin for Cheshire Cat AI that creates related questions from declarative memory. The questions are stored in "relatedquestions" of the Cat reply.

This plugin will create new questions each time the user send a prompt that ends with "?"

Those new questions will be generated starting from the declarative memories in order to have more proper and related topic.

This plugin works particularly well with Cheshire Cat AI installations dedicated to a specific theme, allowing for results that are especially related to the main topic.

Is not really meant for general purpouse case.

In the settings of this plugin you will find the option to set the number of related questions and a couple of threshold.

The first threshold is used to determine how relevant the user's question is to the main theme. If there are declarative memories associated with the prompt but they score lower than the threshold, no new question are generated.

The second threshold is used to make the conversation even more thematic. All prompts that lead to obtaining declarative memories with a score lower than this threshold will result in a negative response from Cheshire Cat AI, which will invite staying on topic. It is possible to specify the text for this response.

[This part of the code is strictly mutuated from Mock Turtle plugin by ironblaster.
https://github.com/ironblaster/mock_turtle]

