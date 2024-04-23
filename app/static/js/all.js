function getCarUrl() {
  const baseUrl = window.location.origin;
  return `${baseUrl}/cars/single`;
}
function displayCars() {
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
        const carUrl = getCarUrl();
        carItem.innerHTML = `
            <div class="card flex-grow-1 d-flex flex-column">
              <div class="card-img">
                <img src="../static/cars-img/${car.car_name}/img_0.jpg" alt="" />
              </div>
                <div class="card-info flex-grow-1 d-flex flex-column">
                  <h4>${car.car_name}</h4>
                  <div class="card-like">
                    <i class="fa fa-heart"></i><span>50</span>
                  </div>
                  <div class="card-icons flex-grow-1">
                    <span class="icon"><img src="../static/images/icons/1.svg" alt="" />${car.seat}</span>
                    <span class="icon"><img src="../static/images/icons/3.svg" alt="" />${car.door}</span>
                    <span class="icon"><img src="../static/images/icons/4.svg" alt="" />${car.body}</span>
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

function displayCarsMenu() {
  fetch("/api/cars")
    .then((response) => response.json())
    .then((data) => {
      const carsMenu = document.getElementById("cars-menu");
      carsMenu.innerHTML = "";
      data.forEach((car, index) => {
        if (index < 12) {
          const carItem = document.createElement("div");
          carItem.classList.add(
            "col-xl-4",
            "col-lg-6",
            "d-flex",
            "flex-column"
          );
          const carUrl = getCarUrl();
          carItem.innerHTML = `
          <div class="de-item mb30 flex-grow-1 d-flex flex-column">
            <div class="d-img">
              <img src="../static/cars-img/${car.car_name}/img_0.jpg" class="img-fluid" alt="${car.car_name}" />
            </div>
            <div class="d-info flex-grow-1 d-flex flex-column">
              <div class="d-text flex-grow-1 d-flex flex-column">
                <h4 class="flex-grow-1">${car.car_name}</h4>
                <div class="d-item_like">
                  <i class="fa fa-heart"></i><span>50</span>
                </div>
                <div class="d-atr-group">
                <span class="d-atr"><img src="../static/images/icons/1.svg" alt="" />${car.seat}</span>
                <span class="d-atr"><img src="../static/images/icons/3.svg" alt="" />${car.door}</span>
                <span class="d-atr"><img src="../static/images/icons/4.svg" alt="" />${car.body}</span>
                </div>
                <div class="d-price">
                  Daily rate from <span>$265</span>
                  <a class="btn-main" href="${carUrl}">Rent Now</a>
                </div>
              </div>
            </div>
          </div>
        `;
          carsMenu.appendChild(carItem);
        }
      });
    })
    .catch((error) => {
      console.error("Error fetching data:", error);
    });
}

window.onload = () => {
  displayCarsMenu();
  displayCars();
};
