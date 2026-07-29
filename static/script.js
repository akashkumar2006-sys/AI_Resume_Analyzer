// AI Resume Analyzer JavaScript
// AI Resume Analyzer JavaScript
// ==========================================
// ResumeIQ AI
// JavaScript - Part 1
// ==========================================

// Show selected file name

const resumeInput = document.getElementById("resume");
const fileName = document.getElementById("file-name");

if (resumeInput) {

    resumeInput.addEventListener("change", function () {

        if (this.files.length > 0) {

            fileName.innerHTML =
                "📄 " + this.files[0].name;

        } else {

            fileName.innerHTML =
                "No file selected";

        }

    });

}

// Drag & Drop Upload

const uploadBox = document.querySelector(".upload-box");

if (uploadBox) {

    uploadBox.addEventListener("dragover", function (e) {

        e.preventDefault();

        uploadBox.style.borderColor = "#4f46e5";

        uploadBox.style.background = "#eef4ff";

    });

    uploadBox.addEventListener("dragleave", function () {

        uploadBox.style.borderColor = "#2563eb";

        uploadBox.style.background = "#ffffff";

    });

    uploadBox.addEventListener("drop", function (e) {

        e.preventDefault();

        uploadBox.style.borderColor = "#2563eb";

        uploadBox.style.background = "#ffffff";

        if (e.dataTransfer.files.length > 0) {

            resumeInput.files = e.dataTransfer.files;

            fileName.innerHTML =
                "📄 " + e.dataTransfer.files[0].name;

        }

    });

}
// ==========================================
// ResumeIQ AI
// JavaScript - Part 2
// ==========================================

// Loading Animation

const uploadForm = document.getElementById("uploadForm");
const analyzeBtn = document.querySelector(".analyze-btn");

if (uploadForm && analyzeBtn) {

    uploadForm.addEventListener("submit", function () {

        analyzeBtn.disabled = true;

        analyzeBtn.innerHTML =
            '<i class="fa-solid fa-spinner fa-spin"></i> Analyzing Resume...';

    });

}

// Animated Statistics Counter

const counters = document.querySelectorAll(".stat-card h2");

const animateCounter = (counter) => {

    const text = counter.innerText;

    if (text.includes("%") || text.includes("+") || text.includes("AI") || text.includes("×")) {
        return;
    }

    const target = Number(text);

    if (isNaN(target)) {
        return;
    }

    let value = 0;

    const speed = Math.max(15, Math.floor(1500 / target));

    const timer = setInterval(() => {

        value++;

        counter.innerText = value;

        if (value >= target) {

            clearInterval(timer);

        }

    }, speed);

};

const observer = new IntersectionObserver((entries) => {

    entries.forEach((entry) => {

        if (entry.isIntersecting) {

            animateCounter(entry.target);

            observer.unobserve(entry.target);

        }

    });

});

counters.forEach((counter) => {

    observer.observe(counter);

});

// Smooth Navigation

document.querySelectorAll('a[href^="#"]').forEach(anchor => {

    anchor.addEventListener("click", function (e) {

        e.preventDefault();

        const target = document.querySelector(this.getAttribute("href"));

        if (target) {

            target.scrollIntoView({

                behavior: "smooth"

            });

        }

    });

});
// ==========================================
// ResumeIQ AI
// JavaScript - Part 3
// ==========================================

// Scroll Reveal Animation

const revealElements = document.querySelectorAll(
    ".feature-card, .step, .stat-card, .about-card, .upload-box"
);

const revealObserver = new IntersectionObserver((entries) => {

    entries.forEach((entry) => {

        if (entry.isIntersecting) {

            entry.target.style.opacity = "1";
            entry.target.style.transform = "translateY(0)";
            revealObserver.unobserve(entry.target);

        }

    });

}, {
    threshold: 0.15
});

revealElements.forEach((element) => {

    element.style.opacity = "0";
    element.style.transform = "translateY(40px)";
    element.style.transition = "all 0.7s ease";

    revealObserver.observe(element);

});

// Scroll To Top Button

const topButton = document.createElement("button");

topButton.innerHTML = "↑";

topButton.id = "topButton";

document.body.appendChild(topButton);

topButton.style.cssText = `
position:fixed;
bottom:25px;
right:25px;
width:55px;
height:55px;
border:none;
border-radius:50%;
background:#2563eb;
color:#fff;
font-size:22px;
cursor:pointer;
display:none;
box-shadow:0 10px 25px rgba(0,0,0,.2);
transition:.3s;
z-index:9999;
`;

window.addEventListener("scroll", () => {

    if (window.scrollY > 300) {

        topButton.style.display = "block";

    } else {

        topButton.style.display = "none";

    }

});

topButton.addEventListener("click", () => {

    window.scrollTo({

        top: 0,
        behavior: "smooth"

    });

});

// Active Navigation Link

const sections = document.querySelectorAll("section");
const navLinks = document.querySelectorAll(".nav-links a");

window.addEventListener("scroll", () => {

    let current = "";

    sections.forEach((section) => {

        const sectionTop = section.offsetTop - 120;

        if (pageYOffset >= sectionTop) {

            current = section.getAttribute("id");

        }

    });

    navLinks.forEach((link) => {

        link.classList.remove("active");

        if (link.getAttribute("href") === "#" + current) {

            link.classList.add("active");

        }

    });

});

console.log("✅ ResumeIQ AI Loaded Successfully");
