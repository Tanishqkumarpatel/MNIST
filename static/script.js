const canvas = document.getElementById('canvas')
const predict_button = document.querySelector('.predict-btn')
const clear_button = document.querySelector('.clear-btn')
const table = document.getElementById('p-table')

const context = canvas.getContext("2d")
context.strokeStyle = "white"
context.fillStyle = "black"
context.lineWidth = 10
context.lineCap = "round"
context.fillRect(0, 0, canvas.width, canvas.height)
let isDrawing = false
let hasDrawn = false

function getMousePos(e) { 
    const rect = canvas.getBoundingClientRect()
    return {
        x: (e.offsetX / rect.width) * canvas.width,
        y: (e.offsetY / rect.height) * canvas.height
    }
}

canvas.addEventListener("mousedown", (e) => {
    isDrawing=true
    context.beginPath()
    const mousePos = getMousePos(e)
    context.moveTo(mousePos.x, mousePos.y)
})

canvas.addEventListener("mouseup", () => {
    isDrawing=false
})

canvas.addEventListener("mousemove", (e) => {
    if (isDrawing) {    
        const mousePos = getMousePos(e)
        context.lineTo(mousePos.x, mousePos.y)
        context.stroke()
        hasDrawn=true
    }
})

canvas.addEventListener("mouseleave", () => {
    isDrawing = false
})

clear_button.addEventListener("click", () => {
    context.clearRect(0,0,canvas.width, canvas.height)
    context.fillRect(0, 0, canvas.width, canvas.height)
    hasDrawn=false
    table.innerHTML=''
})

predict_button.addEventListener("click", () => {
    if (!hasDrawn) return

    canvas.toBlob((blob) => {
        const formData = new FormData()
        formData.append("image", blob, "sketch.png")

        fetch("/predict", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            table.innerHTML = data.probabilities.map((prob, digit) => {
                return `
                <div class="prob-row ${digit === data.prediction ? 'active' : ''}">
                    <span class="prob-digit">${digit}</span>
                    <div class="prob-bar-wrapper">
                        <div class="prob-bar" style="width: ${(prob * 100).toFixed(1)}%"></div>
                    </div>
                    <span class="prob-value">${(prob * 100).toFixed(1)}%</span>
                </div>
            `}).join('')
        })
        .catch(error => console.error(error))
    }, "image/png")
})