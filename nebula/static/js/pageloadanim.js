let loaderDiv = document.createElement("div");
loaderDiv.classList.add("loader");

let ellipsisLoader = document.createElement("div");
ellipsisLoader.classList.add("lds-ellipsis");

for (let i = 0; i < 4; i++) {
	let div = document.createElement("div");
	ellipsisLoader.appendChild(div);
}

loaderDiv.appendChild(ellipsisLoader);
document.documentElement.prepend(loaderDiv);
