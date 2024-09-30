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

document.addEventListener("DOMContentLoaded", () => {
  const bookingForm = document.getElementById("form-booking");

  // 綁定提交表單事件
  bookingForm.addEventListener("submit", async function (e) {
    e.preventDefault();

    const currentDateTime = new Date(new Date().getTime() + 30 * 60 * 1000);
    const pickupDate = document.getElementById("pickup-date").value;
    const pickupTime = document.getElementById("pickup-time").value;
    const returnDate = document.getElementById("return-date").value;
    const returnTime = document.getElementById("return-time").value;
    const pickupDateTime = new Date(`${pickupDate}T${pickupTime}`);
    const returnDateTime = new Date(`${returnDate}T${returnTime}`);

    if (pickupDateTime < currentDateTime || returnDateTime < currentDateTime) {
      alert("Pick-up and return times cannot be before the current time.");
      return;
    }

    if (returnDateTime <= pickupDateTime) {
      alert("Return time cannot be earlier than pick-up time.");
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
        const content = `
          <li class="mb-2">訂單編號：${data.bookingId}</li>
          <li class="mb-2">訂單車輛：${data.carName}</li> 
          <li class="mb-2">客戶名稱：${data.userName}</li>
          <li class="mb-2">取車日期：${data.pickup_date}</li>
          <li class="mb-2">還車日期：${data.return_date}</li>
          <li class="mb-2">取車時間：${data.pickup_time}</li>
          <li class="mb-2">還車時間：${data.return_time}</li>
          <li class="mb-2">取車地點：${data.pickup_loc}</li>
          <li class="mb-2">還車地點：${data.return_loc}</li>
          <li class="mb-2">租用時數：${data.total_hours} 小時</li>
          <li>價錢：${data.total_price} 元</li>
        `;

        document.getElementById("form-order-content").innerHTML = content;
        const modal = new bootstrap.Modal(
          document.getElementById("form-order")
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
          } catch (err) {
            console.error("Error:", error);
            alert("System error, please try again later.");
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
        alert("Please log in!");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("System error, please try again later.");
    }
  });
});
