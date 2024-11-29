import { Streamlit } from "streamlit-component-lib"
import { useRenderData } from "streamlit-component-lib-react-hooks"
import React, { useState, useCallback } from "react"

/**
 * This is a React-based component template with functional component and hooks.
 */
function ImageSelector() {
  // "useRenderData" returns the renderData passed from Python.
  const renderData = useRenderData()

  const [isFocused, setIsFocused] = useState(false)
  const [selected, setSelected] = useState(Array<number>())

  /** Click handler for our "Click Me!" button. */
  const onClicked = useCallback((index: number) => {
    // Increment `numClicks` state, and pass the new value back to
    // Streamlit via `Streamlit.setComponentValue`.
    const newValue = selected.includes(index) ? 
      selected.filter((i) => i !== index) :
      [...selected, index]
    setSelected(newValue)
    Streamlit.setComponentValue(newValue)
  }, [selected])

  /** Focus handler for our "Click Me!" button. */
  const onFocus = useCallback(() => {
    setIsFocused(true)
  }, [])

  /** Blur handler for our "Click Me!" button. */
  const onBlur = useCallback(() => {
    setIsFocused(false)
  }, [])

  // Arguments that are passed to the plugin in Python are accessible
  // via `renderData.args`. Here, we access the "name" arg.
  const images = renderData.args["images"]

  // Streamlit sends us a theme object via renderData that we can use to ensure
  // that our component has visuals that match the active theme in a
  // streamlit app.
  const theme = renderData.theme
  const style: React.CSSProperties = {}

  // Maintain compatibility with older versions of Streamlit that don't send
  // a theme object.
  if (theme) {
    // Use the theme object to style our button border. Alternatively, the
    // theme style is defined in CSS vars.
    //const borderStyling = `1px solid ${isFocused ? theme.primaryColor : "gray"}`
    //style.border = borderStyling
    //style.outline = borderStyling
  }

  // Show a button and some text.
  // When the button is clicked, we'll increment our "numClicks" state
  // variable, and send its new value back to Streamlit, where it'll
  // be available to the Python program.
  return (
    <div className="image-selector" style={style}>
      {
        images.map((image: any, index: number) => (
          <figure
            key={index}
            className={selected.includes(index) ? "selected" : ""}
            onClick={() => onClicked(index)}
            onFocus={onFocus}
            onBlur={onBlur}
          >
            <img src={image.src} alt={image.name} />
            <figcaption>{image.name}</figcaption>
          </figure>
        ))
      }
    </div>
  )
}

export default ImageSelector
