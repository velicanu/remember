import { Streamlit, RenderData } from "streamlit-component-lib"

const span = document.body.appendChild(document.createElement("span"))
const input = span.appendChild(document.createElement("input"))
input.id = "iinput"
input.type = "file"
input.accept = "audio/*"
input.setAttribute("capture", "");

function getBase64(file) {
   var reader = new FileReader();
   reader.readAsDataURL(file);
   reader.onload = function () {
       Streamlit.setComponentValue(reader.result);
   };
   reader.onerror = function (error) {
     console.log('Error: ', error);
   };
}

input.onchange = function(): void {
    var selectedFile = (document.getElementById('iinput') as HTMLInputElement)

    if (selectedFile === null || selectedFile.files === null) {
        // pass
    } else {
        var output =selectedFile.files[0];
        getBase64(output)
           
    }
}

/**
 * The component's render function. This will be called immediately after
 * the component is initially loaded, and then again every time the
 * component gets new data from Python.
 */
function onRender(event: Event): void {
  // Get the RenderData from the event
  const data = (event as CustomEvent<RenderData>).detail

  // RenderData.args is the JSON dictionary of arguments sent from the
  // Python script.
  let name = data.args["name"]

  Streamlit.setFrameHeight()
}
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)
Streamlit.setComponentReady()
Streamlit.setFrameHeight()
