document.addEventListener("DOMContentLoaded", () => {

    const modal = document.getElementById("modal")
    const editBtn = document.getElementById("edit-btn")
    const closeBtn = document.getElementById("close-btn")
    const saveBtn = document.getElementById("save-btn")
    const container = document.getElementById("media-container");

    editBtn.addEventListener("click", () => {
        modal.style.display = "flex";
    });

    closeBtn.addEventListener("click", () => {
        modal.style.display = "none";
    });

    saveBtn.addEventListener("click", async () => {
        const estado = document.getElementById("edit-status").value;
        const puntaje = document.getElementById("edit-score").value;
        const opinion = document.getElementById("edit-review").value;

        let payload = {};

        if (estado !== "") payload.estado = estado;
        if (puntaje !== "") payload.puntaje = puntaje;
        if (opinion !== "") payload.opinion = opinion;

        if (Object.keys(payload).length === 0) {
            modal.style.display = "none";
            return;
        }

        try{
            const itemId = container.dataset.id;
            const response = await fetch(`/actualizar/${itemId}`, {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            });
            
            const data = await response.json();
			
			console.log(data.opinion)

            if (data.estado !== undefined) {
                document.getElementById("user-status").innerText = data.estado;
            }

            if (data.puntaje !== undefined) {
                document.getElementById("user-score").innerText = data.puntaje;
            }

            if (data.opinion !== undefined) {
                document.getElementById("user-review").innerText = data.opinion;
            }

            modal.style.display = "none";
        } catch (error) {
            console.error("Error: ", error);
        }
    });
});