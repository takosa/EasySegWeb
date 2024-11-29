import React from "react"
import ReactDOM from "react-dom"
import { StreamlitProvider } from "streamlit-component-lib-react-hooks"
import ImageSelector from "./ImageSelector"
import "./index.css"

ReactDOM.render(
  <React.StrictMode>
    <StreamlitProvider>
      <ImageSelector />
    </StreamlitProvider>
  </React.StrictMode>,
  document.getElementById("root")
)
