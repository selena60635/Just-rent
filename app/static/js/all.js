function getCarUrl(id) {
  const baseUrl = window.location.origin;
  return `${baseUrl}/car/${id}`;
}
function sliderCars() {
  fetch("/api/cars")
    .then((response) => response.json())
    .then((data) => {
      const carContainer = document.getElementById("items-carousel");
      // 清空容器
      carContainer.innerHTML = "";
      carContainer.classList.add("my-slider");
      data.forEach((car) => {
        const carItem = document.createElement("li");
        carItem.classList.add("d-flex", "flex-column");
        const carUrl = getCarUrl(car.id);
        carItem.innerHTML = `
          <div class="card flex-grow-1 d-flex flex-column">
          <div class="card-img">
          <img src="../static/cars-img/${car.brand}${
          car.year
        }${car.model.replace(/\s/g, "")}/img_0.jpg" alt="" />
        </div>
              <div class="card-info flex-grow-1 d-flex flex-column">
                <h4>${car.car_name}</h4>
                <div class="card-like">
                  <i class="fa fa-heart"></i><span>50</span>
                </div>
                <div class="card-icons flex-grow-1">
                  <span class="icon"><img src="../static/images/icons/1.svg" alt="" />${
                    car.seat
                  }</span>
                  <span class="icon"><img src="../static/images/icons/3.svg" alt="" />${
                    car.door
                  }</span>
                  <span class="icon"><img src="../static/images/icons/4.svg" alt="" />${
                    car.body
                  }</span>
                </div>
                <div class="card-price d-flex justify-content-between align-items-center">
                <div>Daily rate from <span>$265</span></div>
                  <a class="card-btn btn btn-primary font-title fw-800 fs-14 " href="${carUrl}">Rent Now</a>
                </div>
              </div>
            </div>

        `;
        carContainer.appendChild(carItem);
      });
      // 初始化 Tiny Slider
      tns({
        container: ".my-slider",
        items: 3,
        swipeAngle: false,
        speed: 400,
        nav: false,
        gutter: 24,
      });
    })
    .catch((error) => {
      console.error("Error fetching data:", error);
    });
}
