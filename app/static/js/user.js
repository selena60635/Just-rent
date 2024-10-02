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

async function editProfile() {
  const form = document.getElementById("form-create-item");

  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    // 取德表單數據
    const formData = new FormData(this);
    const phone = formData.get("phone");
    const password = formData.get("user_password");
    const rePassword = formData.get("user_password_re-enter");

    // 電話號碼格式驗證
    const phonePattern = /^09\d{8}$/;
    if (!phonePattern.test(phone)) {
      alert("Phone number must be 10 digits and start with 09.");
      return;
    }

    // 密碼驗證
    if (password && password !== rePassword) {
      alert("Passwords do not match.");
      return;
    }

    try {
      const res = await fetch(`/api/user/edit`, {
        method: "POST",
        body: formData,
      });

      const data = await res.json();

      // 處理回傳的狀態碼
      if (res.status === 200) {
        alert(data.message || "Profile updated successfully");
      } else if (res.status === 400 || res.status === 401) {
        alert(data.message || "An error occurred, please check your input");
      }
    } catch (err) {
      console.error("Error:", err);
      alert("An unexpected error occurred. Please try again.");
    }
  });
}

// 初始化表單提交處理
editProfile();
