// 設定 TapPay SDK
TPDirect.setupSDK(
  154236,
  "app_LREPGlLFftNvoS5TmYzIN8IBoH2urewAZ5ybP5idBeqVezujA5E7o4kCRDNd",
  "sandbox"
);

// 設定 TapPay 卡片欄位
TPDirect.card.setup({
  fields: {
    number: {
      element: "#card-number",
      placeholder: "**** **** **** ****",
    },
    expirationDate: {
      element: "#card-expiration-date",
      placeholder: "MM / YY",
    },
    ccv: {
      element: "#card-ccv",
      placeholder: "後三碼",
    },
  },
  styles: {
    input: {
      color: "black",
      "font-size": "16px",
    },
    ".valid": {
      color: "green",
    },
    ".invalid": {
      color: "red",
    },
  },
  isMaskCreditCardNumber: true,
  maskCreditCardNumberRange: {
    beginIndex: 6,
    endIndex: 11,
  },
});

// 監聽 TapPay 欄位的更新狀態
TPDirect.card.onUpdate(function (update) {
  const payButton = document.getElementById("tappay-btn");
  if (update.canGetPrime) {
    payButton.removeAttribute("disabled");
  } else {
    payButton.setAttribute("disabled", true);
  }
});

document
  .getElementById("payment-form")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    TPDirect.card.getPrime(async (result) => {
      if (result.status !== 0) {
        alert("Payment failed, please try again!");
        return;
      }
      //取得 Prime，將 prime 傳送到後端進行付款處理
      const prime = result.card.prime;
      const bookingData = document.getElementById("booking-data");
      const amount = bookingData.dataset.price;
      const bookingId = bookingData.dataset.bookingId;
      // 付款資料
      const paymentData = {
        prime: prime,
        amount: amount,
        booking_id: bookingId,
      };

      // 發送請求到後端 API
      try {
        const res = await fetch("/api/booking/payment", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(paymentData),
        });
        const data = await res.json();
        if (!res.ok) {
          throw new Error(
            data.message || "Payment failed, please try again later."
          );
        }
        alert(`${data.message}`);
        window.location.href = "/orders";
      } catch (err) {
        alert(err.message || "System error, please try again later.");
        if (
          err.message ===
          "Invalid order or this order has already been paid, please do not make duplicate payments."
        ) {
          window.location.href = "/orders";
        }
        console.error("Error:", err);
      }
    });
  });
