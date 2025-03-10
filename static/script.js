document.addEventListener("DOMContentLoaded", function () {
    fetchSeats();
});

function fetchSeats() {
    fetch("http://127.0.0.1:5000/seats")
        .then(response => response.json())
        .then(data => {
            const busLayout = document.getElementById("bus-seats");
            busLayout.innerHTML = "";
            data.forEach(seat => {
                const seatDiv = document.createElement("div");
                seatDiv.className = `seat ${seat.booked ? "booked" : ""}`;
                seatDiv.innerText = seat.number;
                seatDiv.onclick = () => bookSeat(seat.id);
                busLayout.appendChild(seatDiv);
            });
        });
}

function bookSeat(seatId) {
    fetch("http://127.0.0.1:5000/book", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ seat_id: seatId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById("qr-code").src = data.qr_code;
            document.getElementById("qr-container").style.display = "block";
            fetchSeats();
        } else {
            alert(data.message);
        }
    });
}
