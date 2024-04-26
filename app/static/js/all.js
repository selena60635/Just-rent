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

function displayCar(id) {
  fetch(`/api/car/${id}`)
    .then((response) => response.json())
    .then((car) => {
      const imgSlider = document.getElementById("tiny-slider");
      imgSlider.innerHTML = `<div class="my-slider"></div><div class="slider-thumb d-flex"></div>`;
      const bigSlider = imgSlider.querySelector(".my-slider");
      const thumbSlider = imgSlider.querySelector(".slider-thumb");

      for (let i = 0; i < 4; i++) {
        const item = document.createElement("div");
        const img = document.createElement("img");
        const fileName = `${car.brand}${car.year}${car.model.replace(
          /\s/g,
          ""
        )}`;
        img.src = `../static/cars-img/${fileName}/img_${i}.jpg`;
        img.alt = `${fileName}-img${i}`;
        item.appendChild(img);
        bigSlider.appendChild(item);
        const thumbItem = item.cloneNode(true);
        thumbSlider.appendChild(thumbItem);
      }
      imgSlider.appendChild(bigSlider);
      imgSlider.appendChild(thumbSlider);

      const carPrice = document.getElementById("car-price");
      const carSpec = document.getElementById("car-spec");
      carPrice.innerHTML = `Daily rate<h3>${car.price}</h3>`;
      carSpec.innerHTML = `
        <h3>${car.brand} ${car.model}</h3>
        <p></p>
        <div class="spacer-10"></div>
        <h4>Specifications</h4>
        <div class="de-spec">
          <div class="d-row">
            <span class="d-title">Brand</span><span class="d-value">${car.brand}</span>
          </div>
          <div class="d-row">
            <span class="d-title">Model</span><span class="d-value">${car.model}</span>
          </div>
          <div class="d-row">
            <span class="d-title">Body</span><span class="d-value">${car.body}</span>
          </div>
          <div class="d-row">
            <span class="d-title">Seat</span><span class="d-value">${car.seat} seats</span>
          </div>
          <div class="d-row">
            <span class="d-title">Door</span><spam class="d-value">${car.door} doors</spam>
          </div>
          <div class="d-row">
            <span class="d-title">Year</span><span class="d-value">${car.year}</span>
          </div>
          <div class="d-row">
            <span class="d-title">Engine</span><span class="d-value">${car.displacement}</span>
          </div>
          <div class="d-row">
            <span class="d-title">Power type</span><span class="d-value">${car.power_type}</span>
          </div>
          <div class="d-row">
            <span class="d-title">Car Length</span><span class="d-value">${car.car_length}</span>
          </div>
          <div class="d-row">
            <span class="d-title">Wheelbase</span><span class="d-value">${car.wheelbase}</span>
          </div>
        </div>
        <div class="spacer-single"></div>
        <h4>Features</h4>
        <ul class="ul-style-2">
        </ul>
      `;

      // 初始化 Tiny Slider
      tns({
        container: ".my-slider",
        items: 1,
        slideBy: "page",
        navContainer: ".slider-thumb",
        navPosition: "bottom",
        controls: false,
        navAsThumbnails: true,
        speed: 600,
      });
    })
    .catch((error) => {
      console.error("Error fetching data:", error);
    });
}
