function displayBooking() {
  fetch("/api/bookings")
    .then((res) => res.json())
    .then((data) => {
      console.log(data);
      const ordersTable = document.querySelector("#orders-table");
      const ordersTableCompleted = document.querySelector(
        "#orders-table-completed"
      );

      if (ordersTable && ordersTableCompleted) {
        ordersTable.innerHTML = "";
        ordersTableCompleted.innerHTML = "";
        const currentDate = new Date();

        data.forEach((order) => {
          const row = document.createElement("tr");

          if (order.status === "pending") {
            // row.style.cursor = "pointer";
            row.classList.add("pending-row");
            row.onclick = () => {
              window.location.href = `/payment/${order.id}`;
            };
          }

          const orderIdCell = document.createElement("td");
          orderIdCell.innerHTML = `<div class="badge bg-gray-100 text-dark">#${order.id}</div>`;
          row.appendChild(orderIdCell);

          const carNameCell = document.createElement("td");
          carNameCell.innerHTML = `<span class="bold text-truncate" style="max-width: 150px; display: inline-block;">${order.car_name}</span>`;
          row.appendChild(carNameCell);

          const pickupLocationCell = document.createElement("td");
          pickupLocationCell.textContent = order.pickup_location;
          row.appendChild(pickupLocationCell);

          const dropoffLocationCell = document.createElement("td");
          dropoffLocationCell.textContent = order.return_location;
          row.appendChild(dropoffLocationCell);

          const pickupDateCell = document.createElement("td");
          pickupDateCell.textContent = order.pickup_date;
          row.appendChild(pickupDateCell);

          const returnDateCell = document.createElement("td");
          returnDateCell.textContent = order.return_date;
          row.appendChild(returnDateCell);

          const statusCell = document.createElement("td");
          const badge = document.createElement("div");

          const returnDateTime = new Date(
            order.return_date + "T" + order.return_time
          );

          if (returnDateTime < currentDate) {
            badge.classList.add("badge", "rounded-pill", "bg-success");
            badge.textContent = "completed";
            statusCell.appendChild(badge);
            row.appendChild(statusCell);
            ordersTableCompleted.appendChild(row);
          } else if (
            order.status === "pending" ||
            order.status === "scheduled"
          ) {
            badge.classList.add("badge", "rounded-pill", "bg-warning");
            badge.textContent = order.status;
            statusCell.appendChild(badge);
            row.appendChild(statusCell);
            ordersTable.appendChild(row);
          }
        });
      }
    })
    .catch((err) => {
      console.error("Error fetching data:", err);
    });
}

displayBooking();
