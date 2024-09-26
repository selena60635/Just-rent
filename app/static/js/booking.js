// document.addEventListener("DOMContentLoaded", () => {
//   fetch("/api/booking/locations")
//     .then((response) => response.json())
//     .then((data) => {
//       const pickupDatalist = document.getElementById("pickup-locs");
//       const dropoffDatalist = document.getElementById("dropoff-locs");

//       data.forEach((location) => {
//         const option = document.createElement("option");
//         option.value = location;
//         pickupDatalist.appendChild(option);

//         const dropoffOption = option.cloneNode(true);
//         dropoffDatalist.appendChild(dropoffOption);
//       });
//     })
//     .catch((err) => console.error("Error loading locations:", err));
// });

loadLocs();

async function loadLocs() {
  try {
    const response = await fetch("/api/booking/locations");

    if (!response.ok) {
      throw new Error("Network response was not ok");
    }

    const data = await response.json();
    const pickupDatalist = document.getElementById("pickup-locs");
    const dropoffDatalist = document.getElementById("dropoff-locs");

    data.forEach((location) => {
      const option = document.createElement("option");
      option.value = location;
      pickupDatalist.appendChild(option);

      const dropoffOption = option.cloneNode(true);
      dropoffDatalist.appendChild(dropoffOption);
    });
  } catch (err) {
    console.error("Error loading locations:", err);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  // 初始化 pick up 日期選擇器
  $("#pickup-date").datepicker({
    format: "yyyy-mm-dd",
    startDate: new Date(),
    autoclose: true,
    todayHighlight: true,
  });

  // 初始化 return 日期選擇器
  $("#return-date").datepicker({
    format: "yyyy-mm-dd",
    startDate: new Date(),
    autoclose: true,
    todayHighlight: true,
  });
});
// document.addEventListener("DOMContentLoaded", () => {
//   const bookingForm = document.querySelector("form");

//   bookingForm.addEventListener("submit", (e) => {
//     e.preventDefault();
//     // const pickupLoc = document.getElementById("pickup").value;
//     // const dropoffLoc = document.getElementById("dropoff").value;

//     const pickupDate = document.getElementById("pickup-date").value;
//     const pickupTime = document.getElementById("pickup-time").value;
//     const returnDate = document.getElementById("return-date").value;
//     const returnTime = document.getElementById("return-time").value;
//     const pickupDateTime = new Date(`${pickupDate}T${pickupTime}`);
//     const returnDateTime = new Date(`${returnDate}T${returnTime}`);

//     // if (pickupLoc === dropoffLoc) {
//     //   alert("Pick Up Location and Drop Off Location cannot be the same.");
//     //   return;
//     // }

//     if (returnDateTime <= pickupDateTime) {
//       alert("Return Date & Time cannot be earlier than Pick Up Date & Time.");
//       return;
//     }

//     bookingForm.submit();
//   });
// });

document.addEventListener("DOMContentLoaded", () => {
  const bookingForm = document.getElementById("form-booking");

  // 綁定提交表單事件
  bookingForm.addEventListener("submit", async function (e) {
    e.preventDefault();

    const currentDateTime = new Date();
    const pickupDate = document.getElementById("pickup-date").value;
    const pickupTime = document.getElementById("pickup-time").value;
    const returnDate = document.getElementById("return-date").value;
    const returnTime = document.getElementById("return-time").value;
    const pickupDateTime = new Date(`${pickupDate}T${pickupTime}`);
    const returnDateTime = new Date(`${returnDate}T${returnTime}`);

    if (pickupDateTime < currentDateTime || returnDateTime < currentDateTime) {
      alert("取車和還車時間不能在當前時間之前");
      return;
    }

    if (returnDateTime <= pickupDateTime) {
      alert("還車時間不能早於取車時間");
      return;
    }

    // 表單檢查通過後進行資料提交
    const formData = new FormData(this);

    try {
      const response = await fetch("/api/booking/order", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (data.bookingId) {
        const details = `
          <strong>訂單號碼:</strong> ${data.bookingId}<br>
          <strong>訂單車輛:</strong> ${data.carName}<br>
          <strong>使用者:</strong> ${data.userName}<br>
          <strong>建立時間:</strong> ${data.created_at}<br>
          <strong>取車日期:</strong> ${data.pickup_date}<br>
          <strong>還車日期:</strong> ${data.return_date}<br>
          <strong>取車時間:</strong> ${data.pickup_time}<br>
          <strong>還車時間:</strong> ${data.return_time}<br>
          <strong>取車地點:</strong> ${data.pickup_loc}<br>
          <strong>還車地點:</strong> ${data.return_loc}<br>
          <strong>價錢:</strong> ${data.price}<br>
          <strong>狀態:</strong> ${data.status}<br>
        `;

        document.getElementById("modalBookingDetails").innerHTML = details;
        const modal = new bootstrap.Modal(
          document.getElementById("orderSuccessModal")
        );
        modal.show();

        const handlePayment = () => {
          window.location.href = `/payment/${data.bookingId}`;
          removeEventListeners();
        };

        const handleCancel = async () => {
          try {
            const cancelResponse = await fetch(
              `/api/booking/cancel_order/${data.bookingId}`,
              {
                method: "POST",
              }
            );

            const result = await cancelResponse.json();

            if (result.message) {
              alert(result.message);
              modal.hide();
              removeEventListeners(); // 移除事件
            } else if (result.error) {
              alert(result.error);
            }
          } catch (error) {
            console.error("Error:", error);
            alert("系統錯誤，請稍後再試。");
          }
        };

        document
          .getElementById("pay-button")
          .addEventListener("click", handlePayment);
        document
          .getElementById("cancel-button")
          .addEventListener("click", handleCancel);

        function removeEventListeners() {
          document
            .getElementById("pay-button")
            .removeEventListener("click", handlePayment);
          document
            .getElementById("cancel-button")
            .removeEventListener("click", handleCancel);
        }
      } else if (data.error) {
        alert(data.error);
      } else if (data.status === "noauth") {
        alert("請先登入！");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("系統錯誤，請稍後再試。");
    }
  });
});
