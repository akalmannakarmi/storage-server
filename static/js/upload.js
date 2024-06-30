function initializeDragDrop() {
	const fileDropzone = document.getElementById('file-dropzone');
	const folderDropzone = document.getElementById('folder-dropzone');
	const fileInput = document.getElementById('file-input');
	const folderInput = document.getElementById('folder-input');
	const selectedFiles = document.getElementById('selected-files');

	function handleFileSelect(files) {
			selectedFiles.innerHTML = '';
			for (let i = 0; i < files.length; i++) {
					const filePath = files[i].webkitRelativePath || files[i].name;
					selectedFiles.innerHTML += `<p>${filePath}</p>`;
			}
	}

	function handleDragOver(event) {
			event.preventDefault();
			event.currentTarget.classList.add('dragging');
	}

	function handleDragLeave(event) {
			event.currentTarget.classList.remove('dragging');
	}

	function handleFileDrop(event) {
			event.preventDefault();
			event.currentTarget.classList.remove('dragging');
			const files = event.dataTransfer.files;
			fileInput.files = files;
			handleFileSelect(files);
	}

	function handleFolderDrop(event) {
			event.preventDefault();
			event.currentTarget.classList.remove('dragging');
			const items = event.dataTransfer.items;
			const files = [];
			const relativePaths = [];

			for (let i = 0; i < items.length; i++) {
					const item = items[i].webkitGetAsEntry();
					if (item) {
							traverseFileTree(item, '', files, relativePaths);
					}
			}

			setTimeout(() => {
					handleFileSelectWithPaths(files, relativePaths);
					const dataTransfer = new DataTransfer();
					for (let i = 0; i < files.length; i++) {
							const file = new File([files[i]], relativePaths[i]);
							dataTransfer.items.add(file);
					}
					folderInput.files = dataTransfer.files;
			}, 100);
	}

	function traverseFileTree(item, path, files, relativePaths) {
			if (item.isFile) {
					item.file(file => {
							files.push(file);
							relativePaths.push(path + file.name);
					});
			} else if (item.isDirectory) {
					const dirReader = item.createReader();
					dirReader.readEntries(entries => {
							for (let i = 0; i < entries.length; i++) {
									traverseFileTree(entries[i], path + item.name + '/', files, relativePaths);
							}
					});
			}
	}

	function handleFileSelectWithPaths(files, relativePaths) {
			selectedFiles.innerHTML = '';
			for (let i = 0; i < files.length; i++) {
					selectedFiles.innerHTML += `<p>${relativePaths[i]}</p>`;
			}
	}

	// Event listeners for file dropzone
	fileDropzone.addEventListener('dragover', handleDragOver);
	fileDropzone.addEventListener('dragleave', handleDragLeave);
	fileDropzone.addEventListener('drop', handleFileDrop);
	fileDropzone.addEventListener('click', () => fileInput.click());

	// Event listeners for folder dropzone
	folderDropzone.addEventListener('dragover', handleDragOver);
	folderDropzone.addEventListener('dragleave', handleDragLeave);
	folderDropzone.addEventListener('drop', handleFolderDrop);
	folderDropzone.addEventListener('click', () => folderInput.click());

	// Event listeners for file input changes
	fileInput.addEventListener('change', (event) => handleFileSelect(event.target.files));
	folderInput.addEventListener('change', (event) => handleFileSelect(event.target.files));
}

initializeDragDrop()