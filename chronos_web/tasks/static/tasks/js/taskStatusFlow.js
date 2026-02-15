async function updateStatus(url, status, taskId, csrftoken) {
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
    document.getElementById("taskStatus").textContent = data["newStatus"];
    document.getElementById("taskStatus").className =
      `status-${data["newStatus"]}`;
  }
}
