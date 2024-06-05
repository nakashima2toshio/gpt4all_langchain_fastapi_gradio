import gradio as gr


def function_list(name, intensity):
    return "Hello, " + name + "!" * int(intensity)


demo = gr.Interface(
    fn=function_list,
    inputs=["text", "slider"],
    outputs=["text"],
)

demo.launch()
