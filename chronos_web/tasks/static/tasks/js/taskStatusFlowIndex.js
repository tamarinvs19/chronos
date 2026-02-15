async function updateStatus(url, status, taskId, elementId, csrftoken) {
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    mode: "same-origin",
    body: JSON.stringify({ task_id: taskId, status: status }),
  });
  const data = await response.json();
  if (data["status"] === "ok") {
    const elements = document.getElementsByClassName(elementId);
    for (let element of elements) {
      for (let className of element.classList) {
        if (className.startsWith("status")) {
          element.classList.remove(className);
        }
      }
      element.classList.add(`status-${data["newStatus"]}`);
    }
  }
}
