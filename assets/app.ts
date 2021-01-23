const formInputFiles = document.querySelectorAll<HTMLElement>('.form input[type=file]')
formInputFiles.forEach(input => {
  input.addEventListener('change', evt => {
    const file = (evt.target as HTMLInputElement).files[0]
    if (file) {
      const parent = input.parentElement
      const labelElement = parent.querySelector('label')
      labelElement.textContent = 'Change Image'

      const imageContent = parent.querySelector('.image-content')
      const imageEl = imageContent.querySelector('img')

      const reader = new FileReader();
      reader.onloadend = () => {
        const base64 = reader.result
        if (imageEl) {
          imageEl.src = base64 as string
        }
        else {
          const newImageEl = document.createElement('img')
          newImageEl.src = base64 as string
          imageContent.append(newImageEl)
        }
      };
      reader.readAsDataURL(file);
    }
  })
})