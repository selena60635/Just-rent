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
      data.cars.forEach((car) => {
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
                <h4>${car.name}</h4>
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

let currentPage = 1;
let currentFilters = "";

// filter
function applyFilters() {
  currentPage = 1;
  let filters = [];

  // body
  const bodyFilters = [];
  const bodyInputs = document.querySelectorAll(
    "#car-body input[type=checkbox]"
  );

  bodyInputs.forEach((input) => {
    if (input.checked) {
      if (input.id === "other-bodies-filter") {
        bodyFilters.push("other");
      } else {
        bodyFilters.push(input.value);
      }
    }
  });

  if (bodyFilters.length > 0) {
    const bodyFiltersStr = bodyFilters.join(",");
    filters.push(`&body=${bodyFiltersStr}`);
  }

  // seat
  const seatFilters = [];
  const seatInputs = document.querySelectorAll(
    "#car-seat input[type=checkbox]"
  );
  seatInputs.forEach((input) => {
    if (input.checked) {
      seatFilters.push(input.value);
    }
  });
  if (seatFilters.length > 0) {
    const seatFilterStr = seatFilters.join(",");
    filters.push(`&seat=${seatFilterStr}`);
  }
  console.log(bodyFilters);

  // engine
  const engineFilters = [];
  const engineInputs = document.querySelectorAll(
    "#car-displacement input[type=checkbox]"
  );
  engineInputs.forEach((input) => {
    if (input.checked) {
      engineFilters.push(input.value);
    }
  });

  if (engineFilters.length > 0) {
    const engineFilterStr = engineFilters.join(",");
    filters.push(`&engine=${engineFilterStr}`);
  }

  // Price
  const maxPrice = document.querySelector(".input-max").value;
  filters.push(`&max_price=${maxPrice}`);
  // 篩選條件發生變化時重新顯示汽車列表
  currentFilters = filters.join(","); // 將當前的篩選條件保存
  displayCars(currentPage, currentFilters);
  displayCarList(currentPage, currentFilters);
}

// loading cars
function displayCars(pageNumber, filterParams) {
  let url;
  if (filterParams) {
    url = `/api/cars?page=${pageNumber}${filterParams}`;
  } else {
    url = `/api/cars?page=${pageNumber}`;
  }

  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      const carsMenu = document.getElementById("cars-menu");
      if (carsMenu) {
        carsMenu.innerHTML = "";

        if (!data.has_next) {
          document.getElementById("next-page-btn").disabled = true;
        } else {
          document.getElementById("next-page-btn").disabled = false;
        }

        console.log(data.cars.length);

        data.cars.forEach((car) => {
          const carItem = document.createElement("div");
          carItem.classList.add(
            "col-xl-4",
            "col-lg-6",
            "d-flex",
            "flex-column"
          );
          const carUrl = getCarUrl(car.id);
          carItem.innerHTML = `
            <div class="de-item mb30 flex-grow-1 d-flex flex-column">
              <div class="d-img">
                <img src="../static/cars-img/${car.brand}${
            car.year
          }${car.model.replace(/\s/g, "")}/img_0.jpg" alt="${car.name}" />
              </div>
              <div class="d-info flex-grow-1 d-flex flex-column">
                <div class="d-text flex-grow-1 d-flex flex-column">
                  <h4 class="flex-grow-1">${car.name}</h4>
                  <div class="d-item_like">
                    <i class="fa fa-heart"></i><span>50</span>
                  </div>
                  <div class="d-atr-group">
                    <span class="d-atr"><img src="../static/images/icons/1.svg" alt="" />${
                      car.seat
                    }</span>
                    <span class="d-atr"><img src="../static/images/icons/3.svg" alt="" />${
                      car.door
                    }</span>
                    <span class="d-atr"><img src="../static/images/icons/4.svg" alt="" />${
                      car.body
                    }</span>
                  </div>
                  <div class="d-price">
                    Daily rate from <span>$${car.price}</span>
                    <a class="btn-main" href="${carUrl}">Rent Now</a>
                  </div>
                </div>
              </div>
            </div>
          `;
          carsMenu.appendChild(carItem);
        });
      }
    })
    .catch((error) => {
      console.error("Error fetching data:", error);
    });
}
function displayCarList(pageNumber, filterParams) {
  let url;
  if (filterParams) {
    url = `/api/cars?page=${pageNumber}${filterParams}`;
  } else {
    url = `/api/cars?page=${pageNumber}`;
  }
  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      const carsList = document.getElementById("cars-list");
      if (carsList) {
        carsList.innerHTML = "";
        if (!data.has_next) {
          document.getElementById("next-page-btn").disabled = true;
        } else {
          document.getElementById("next-page-btn").disabled = false;
        }
        data.cars.forEach((car) => {
          const carItem = document.createElement("div");
          carItem.classList.add("col-lg-12");
          const carUrl = getCarUrl(car.id);
          carItem.innerHTML = `
              <div class="de-item-list mb30">
              <div class="d-img">
                <img src="../static/cars-img/${car.brand}${
            car.year
          }${car.model.replace(/\s/g, "")}/img_0.jpg" class="img-fluid" alt="${
            car.name
          }" />
              </div>
              <div class="d-info">
                <div class="d-text">
                  <h4>${car.name}</h4>
                  <div class="d-atr-group">
                    <ul class="d-atr">
                      <li><span>Type:</span>${car.body}</li>
                      <li><span>Seats:</span>${car.seat}</li>
                      <li><span>Doors:</span>${car.door}</li>
                      <li><span>Year:</span>${car.year}</li>
                      <li><span>Fuel:</span>${car.power_type}</li>
                      <li><span>Engine:</span>${car.displacement}</li>
                      <li><span>Car length:</span>${car.car_length}</li>
                      <li><span>Wheelbase:</span>${car.wheelbase}</li>
                    </ul>
                  </div>
                </div>
              </div>
              <div class="d-price">
                Daily rate from <span>$${car.price}</span>
                <a
                  class="btn-main"
                  href="${carUrl}"
                  >Rent Now</a
                >
              </div>
              <div class="clearfix"></div>
            </div>`;
          carsList.appendChild(carItem);
        });
      }
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
      carPrice.innerHTML = `Daily rate<h3>$${car.price}</h3>`;
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

// pagination
function prevPage() {
  if (currentPage > 1) {
    currentPage--;
    displayCars(currentPage, currentFilters);
    displayCarList(currentPage, currentFilters);
  }
}

function nextPage() {
  currentPage++;
  displayCars(currentPage, currentFilters);
  displayCarList(currentPage, currentFilters);
}
// 上傳圖片
async function uploadImage() {
  try {
    const formData = new FormData(document.getElementById("uploadForm"));
    const response = await fetch("/api/upload", {
      method: "POST",
      body: formData,
    });
    const data = await response.json();
    const imageUrl = data.url;
    document.getElementById(
      "imageUrl"
    ).innerHTML = `<a href="${imageUrl}" target="_blank">${imageUrl}</a>`;
  } catch (error) {
    console.error("Error:", error);
  }
}
