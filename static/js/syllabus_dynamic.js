document.addEventListener('DOMContentLoaded', function () {
    const syllabusFields = document.querySelectorAll('textarea[id^="id_syllabus_"]');

    syllabusFields.forEach(field => {
        console.log("Found syllabus field:", field.id);
        field.style.display = 'none';

        // Create container and Add Week button
        const container = document.createElement('div');
        container.id = `container-${field.id}`;
        field.parentNode.insertBefore(container, field.nextSibling);

        const addBtn = document.createElement('button');
        addBtn.textContent = '+ Add Week';
        addBtn.type = 'button';
        addBtn.className = 'btn btn-primary mb-3';
        container.appendChild(addBtn);

        const weeksDiv = document.createElement('div');
        container.appendChild(weeksDiv);

        // Parse JSON safely
        let data = [];
        try {
            data = JSON.parse(field.value || '[]');
        } catch (e) {
            console.warn('Invalid JSON in', field.id);
            data = [];
        }

        function updateField() {
            field.value = JSON.stringify(data);
        }

        function render() {
            weeksDiv.innerHTML = '';
            data.forEach((week, idx) => {
                const div = document.createElement('div');
                div.classList.add('p-3', 'mb-3', 'border', 'rounded');
                div.style.background = '#f8f9fa';

                div.innerHTML = `
                    <label><b>Week ${idx + 1} Title:</b></label>
                    <input type="text" class="form-control mb-2 week-title" value="${week.title || ''}" />
                    <label><b>Description:</b></label>
                    <textarea class="form-control week-desc" rows="10">${week.description || ''}</textarea>
                    <button type="button" class="btn btn-danger btn-sm mt-2 remove-week">Remove</button>
                `;

                weeksDiv.appendChild(div);

                const descTextarea = div.querySelector('.week-desc');

                if (window.ClassicEditor) {
                    window.ClassicEditor
                        .create(descTextarea, {
                            licenseKey: 'GPL',
                            // ✅ Upload support
                            simpleUpload: {
                                uploadUrl: '/ckeditor5/upload/',
                                withCredentials: true,
                                headers: { 'X-CSRFToken': getCookie('csrftoken') }
                            },
                            // ✅ Toolbar (same as extends)
                            toolbar: {
                                items: [
                                    'heading', '|', 'outdent', 'indent', '|',
                                    'bold', 'italic', 'link', 'underline', 'strikethrough',
                                    'code', 'subscript', 'superscript', 'highlight', '|',
                                    'codeBlock', 'sourceEditing', 'insertImage',
                                    'bulletedList', 'numberedList', 'todoList', '|',
                                    'blockQuote', 'imageUpload', '|',
                                    'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor',
                                    'mediaEmbed', 'removeFormat', 'insertTable',
                                    '|', 'undo', 'redo'
                                ],
                                shouldNotGroupWhenFull: true
                            },
                            // ✅ Image toolbar
                            image: {
                                toolbar: [
                                    'imageTextAlternative', '|',
                                    'imageStyle:alignLeft', 'imageStyle:alignCenter',
                                    'imageStyle:alignRight', 'imageStyle:side', '|'
                                ],
                                styles: ['full', 'side', 'alignLeft', 'alignRight', 'alignCenter']
                            },
                            // ✅ Table support
                            table: {
                                contentToolbar: [
                                    'tableColumn', 'tableRow', 'mergeTableCells',
                                    'tableProperties', 'tableCellProperties'
                                ]
                            },
                            heading: {
                                options: [
                                    { model: 'paragraph', title: 'Paragraph', class: 'ck-heading_paragraph' },
                                    { model: 'heading1', view: 'h1', title: 'Heading 1', class: 'ck-heading_heading1' },
                                    { model: 'heading2', view: 'h2', title: 'Heading 2', class: 'ck-heading_heading2' },
                                    { model: 'heading3', view: 'h3', title: 'Heading 3', class: 'ck-heading_heading3' }
                                ]
                            },
                            list: {
                                properties: {
                                    styles: true,
                                    startIndex: true,
                                    reversed: true
                                }
                            },
                            fontSize: {
                                options: [10, 12, 14, 'default', 18, 20, 22, 24, 28],
                                supportAllValues: true
                            },
                            fontFamily: {
                                options: ['default', 'Arial', 'Helvetica', 'Georgia', 'Times New Roman', 'Courier New'],
                                supportAllValues: true
                            }
                        })
                        .then(editor => {
                            editor.model.document.on('change:data', () => {
                                week.description = editor.getData();
                                updateField();
                            });
                        })
                        .catch(err => console.error('CKEditor init error:', err));
                } else {
                    console.error('❌ ClassicEditor is not available.');
                }

                // Title handling
                div.querySelector('.week-title').addEventListener('input', e => {
                    week.title = e.target.value;
                    updateField();
                });

                // Remove button
                div.querySelector('.remove-week').addEventListener('click', () => {
                    data.splice(idx, 1);
                    render();
                    updateField();
                });
            });
        }

        addBtn.addEventListener('click', () => {
            data.push({ title: '', description: '' });
            render();
            updateField();
        });

        render();
    });

    // ✅ Helper for CSRF
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
