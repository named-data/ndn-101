/**
 * Get iframe by event
 * @param {MessageEvent} event
 * @returns {HTMLIFrameElement}
 */
function getFrameByEvent(event) {
  return Array.from(document.getElementsByTagName("iframe")).filter(
    (iframe) => {
      return iframe.contentWindow === event.source;
    }
  )[0];
}

/**
 * Handle message from child
 * @param {MessageEvent} event
 */
function handleIframeMessage(event) {
  const frame = getFrameByEvent(event);
  const funcName = frame?.attributes?.getNamedItem("data-message-fun")?.value;
  if (funcName && window[funcName]) {
    window[funcName](event, frame);
  }
}

// Add listener for all messages from children
window.addEventListener("message", handleIframeMessage);

/**
 * Handle message from NDN play visualizer
 * @param {MessageEvent} event
 * @param {HTMLIFrameElement} frame
 */
function handleVisMessage(event, frame) {
  if (event.data.visHeight) {
    frame.style.height = event.data.visHeight + "px";
  }
}
