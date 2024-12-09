const token = localStorage.getItem("token");

// Si no hay token, redirige al login
if (!token) {
    window.location.href = "login.html";
}

// Función para obtener y mostrar las citas
async function fetchAppointments() {
    try {
        const response = await fetch("http://127.0.0.1:5000/appointments", {
            method: "GET",
            headers: { Authorization: `Bearer ${token}` },
        });

        if (!response.ok) {
            console.error("Error al obtener citas:", await response.text());
            alert("Error al cargar citas");
            return;
        }

        const appointments = await response.json();
        console.log("Citas obtenidas:", appointments);

        const list = document.getElementById("appointmentsList");
        list.innerHTML = ""; // Limpia la lista de citas

        if (appointments.length === 0) {
            // Mostrar mensaje si no hay citas
            list.innerHTML = "<li class='list-group-item text-center'>No hay citas disponibles para el usuario</li>";
            return;
        }

        // Renderizar las citas obtenidas
        appointments.forEach((appt) => {
            const li = document.createElement("li");
            li.className = "list-group-item d-flex justify-content-between align-items-center";
            li.innerHTML = `
                <span><strong>${appt.date}:</strong> ${appt.description}</span>
                <div>
                    <button class="btn btn-sm btn-warning edit-btn" data-id="${appt._id}">Editar</button>
                    <button class="btn btn-sm btn-danger delete-btn" data-id="${appt._id}">Borrar</button>
                </div>
            `;
            list.appendChild(li);
        });

        // Agregar eventos a los botones de eliminar y editar
        document.querySelectorAll(".delete-btn").forEach((button) =>
            button.addEventListener("click", deleteAppointment)
        );

        document.querySelectorAll(".edit-btn").forEach((button) =>
            button.addEventListener("click", editAppointment)
        );
    } catch (error) {
        console.error("Error al cargar citas:", error);
        alert("Hubo un error al cargar las citas");
    }
}

// Función para crear una nueva cita
document.getElementById("appointmentForm").addEventListener("submit", async (e) => {
    e.preventDefault(); // Evitar recargar la página al enviar el formulario

    const date = document.getElementById("date").value;
    const description = document.getElementById("description").value;

    if (!date || !description) {
        alert("Por favor, completa todos los campos");
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:5000/appointments", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({ date, description }),
        });

        if (!response.ok) {
            console.error("Error al crear cita:", await response.text());
            alert("Error al crear la cita");
            return;
        }

        alert("Cita creada exitosamente");
        fetchAppointments(); // Recargar las citas después de crear una
    } catch (error) {
        console.error("Error al crear cita:", error);
        alert("Hubo un error al crear la cita");
    }
});

// Función para eliminar una cita
async function deleteAppointment(e) {
    const appointmentId = e.target.dataset.id;
    const confirmDelete = confirm("¿Estás seguro de que quieres borrar esta cita?");
    if (!confirmDelete) return;

    try {
        const response = await fetch(`http://127.0.0.1:5000/appointments/${appointmentId}`, {
            method: "DELETE",
            headers: { Authorization: `Bearer ${token}` },
        });

        if (!response.ok) {
            console.error("Error al borrar cita:", await response.text());
            alert("Error al borrar la cita");
            return;
        }

        alert("Cita borrada exitosamente");
        fetchAppointments(); // Recargar las citas después de eliminar una
    } catch (error) {
        console.error("Error al borrar cita:", error);
        alert("Hubo un error al borrar la cita");
    }
}

// Función para editar una cita
async function editAppointment(e) {
    const appointmentId = e.target.dataset.id;
    const newDate = prompt("Introduce la nueva fecha (YYYY-MM-DD):");
    const newDescription = prompt("Introduce la nueva descripción:");
    if (!newDate || !newDescription) return;

    try {
        const response = await fetch(`http://127.0.0.1:5000/appointments/${appointmentId}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({ date: newDate, description: newDescription }),
        });

        if (!response.ok) {
            console.error("Error al actualizar cita:", await response.text());
            alert("Error al actualizar la cita");
            return;
        }

        alert("Cita actualizada exitosamente");
        fetchAppointments(); // Recargar las citas después de editar una
    } catch (error) {
        console.error("Error al actualizar cita:", error);
        alert("Hubo un error al actualizar la cita");
    }
}

// Cerrar sesión
document.getElementById("logoutButton").addEventListener("click", () => {
    localStorage.removeItem("token");
    window.location.href = "login.html";
});

// Llamar a la función para cargar las citas al cargar la página
fetchAppointments();
