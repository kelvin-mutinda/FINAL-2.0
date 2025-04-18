// luminous_clinic_project/luminous_clinic/static/js/patient_dashboard.js

document.addEventListener('DOMContentLoaded', function() {
    loadContent('home');
});

function loadContent(section) {
    const contentDiv = document.getElementById('main-content');
    switch (section) {
        case 'home':
            contentDiv.innerHTML = `
                <h1>Home</h1>
                <p>Welcome to your patient dashboard!</p>
                <div class="summary-widgets">
                    <div class="widget">
                        <h2>Upcoming Appointments</h2>
                        <p>{{ pending_bookings.count }}</p>
                    </div>
                    <div class="widget">
                        <h2>Active Consultations</h2>
                        <p>{{ accepted_bookings.count }}</p>
                    </div>
                    <div class="widget">
                        <h2>Payments Due</h2>
                        <p>0</p>
                    </div>
                </div>
                <button class="quick-consult">Quick Consult</button>
            `;
            break;
        case 'consult-doctor':
            contentDiv.innerHTML = `
                <h1>Consult a Doctor</h1>
                <div class="service-cards">
                    {% for service in services %}
                        <div class="service-card">
                            <h3>{{ service.service_name }}</h3>
                            <p>{{ service.description }}</p>
                            <button onclick="bookService({{ service.pk }})">Book Now</button>
                        </div>
                    {% endfor %}
                </div>
            `;
            break;
        case 'my-appointments':
            contentDiv.innerHTML = `
                <h1>My Appointments</h1>
                <div class="tabs">
                    <button onclick="showTab('upcoming')">Upcoming</button>
                    <button onclick="showTab('past')">Past</button>
                </div>
                <div id="upcoming" class="tab-content">
                    <h2>Upcoming Appointments</h2>
                    <ul>
                        {% for booking in pending_bookings %}
                            <li>
                                <strong>{{ booking.service.service_name }}</strong> - {{ booking.timestamp|date:"d M. Y" }}
                                <button onclick="cancelBooking({{ booking.id }})">Cancel</button>
                            </li>
                        {% endfor %}
                    </ul>
                </div>
                <div id="past" class="tab-content" style="display: none;">
                    <h2>Past Appointments</h2>
                    <ul>
                        {% for booking in accepted_bookings %}
                            <li>
                                <strong>{{ booking.service.service_name }}</strong> - {{ booking.timestamp|date:"d M. Y" }}
                                <a href="{% url 'chat' booking_id=booking.pk %}">View Details</a>
                            </li>
                        {% endfor %}
                    </ul>
                </div>
            `;
            break;
        case 'active-consultation':
            contentDiv.innerHTML = `
                <h1>Active Consultation</h1>
                <div id="chat-box">
                    <ul id="messages">
                        {% for message in active_consultation.messages.all %}
                            <li class="{{ message.sender.role }}">
                                <strong>{{ message.sender.full_name }}:</strong> {{ message.message }}<br>
                                <small>{{ message.timestamp|date:"d M. Y H:i" }}</small>
                            </li>
                        {% endfor %}
                    </ul>
                </div>
                <form id="chat-form">
                    <input type="text" id="message-input" placeholder="Type a message..." required>
                    <button type="submit">Send</button>
                </form>
                <button onclick="endService()">End Consultation</button>
            `;
            break;
        case 'payments':
            contentDiv.innerHTML = `
                <h1>Payments</h1>
                <table>
                    <thead>
                        <tr>
                            <th>Transaction ID</th>
                            <th>Amount</th>
                            <th>Status</th>
                            <th>Method</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for payment in payments %}
                            <tr>
                                <td>{{ payment.transaction_id }}</td>
                                <td>{{ payment.amount }}</td>
                                <td>{{ payment.payment_status }}</td>
                                <td>{{ payment.method }}</td>
                                <td>
                                    <button>Pay Now</button>
                                    <button>Download Receipt</button>
                                </td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            `;
            break;
        case 'my-notes':
            contentDiv.innerHTML = `
                <h1>My Notes</h1>
                <form id="note-form">
                    <textarea id="note-input" placeholder="Write a note..."></textarea>
                    <button type="submit">Add Note</button>
                </form>
                <ul id="notes-list">
                    {% for note in notes %}
                        <li>
                            <p>{{ note.text }}</p>
                            <button onclick="editNote({{ note.pk }})">Edit</button>
                            <button onclick="deleteNote({{ note.pk }})">Delete</button>
                        </li>
                    {% endfor %}
                </ul>
            `;
            break;
        case 'my-profile':
            contentDiv.innerHTML = `
                <h1>My Profile</h1>
                <form method="post" enctype="multipart/form-data">
                    {% csrf_token %}
                    {{ form.as_p }}
                    <button type="submit">Save</button>
                </form>
                <h2>Medical History</h2>
                <ul>
                    {% for record in medical_records %}
                        <li>{{ record.findings }} - {{ record.timestamp|date:"d M. Y" }}</li>
                    {% endfor %}
                </ul>
                <h2>Change Password</h2>
                <form id="change-password-form">
                    <input type="password" id="current-password" placeholder="Current Password" required>
                    <input type="password" id="new-password" placeholder="New Password" required>
                    <input type="password" id="confirm-password" placeholder="Confirm Password" required>
                    <button type="submit">Change Password</button>
                </form>
            `;
            break;
    }
}

function showTab(tabName) {
    const tabs = document.getElementsByClassName('tab-content');
    for (let i = 0; i < tabs.length; i++) {
        tabs[i].style.display = 'none';
    }
    document.getElementById(tabName).style.display = 'block';
}

function bookService(serviceId) {
    window.location.href = `{% url 'book_service' service_id=serviceId %}`;
}

function cancelBooking(bookingId) {
    fetch(`/cancel-booking/${bookingId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.reload();
        } else {
            alert('Failed to cancel booking');
        }
    });
}

function endService() {
    fetch(`/end-service/${active_consultation.pk}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = '{% url "patient_dashboard" %}';
        } else {
            alert('Failed to end service');
        }
    });
}

function editNote(noteId) {
    alert('Editing note ' + noteId);
}

function deleteNote(noteId) {
    alert('Deleting note ' + noteId);
}

// Add this to your patient_dashboard.js file
document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const appHeader = document.querySelector('.app-header');
    
    // Create mobile toggle button
    const mobileToggle = document.createElement('div');
    mobileToggle.className = 'mobile-toggle';
    mobileToggle.innerHTML = '☰';
    document.body.appendChild(mobileToggle);
    
    // Add click event
    mobileToggle.addEventListener('click', function() {
        const sidebar = document.querySelector('.sidebar');
        sidebar.classList.toggle('show');
    });
    
    // Close sidebar when clicking on a link (mobile)
    const sidebarLinks = document.querySelectorAll('.sidebar a');
    sidebarLinks.forEach(link => {
        link.addEventListener('click', function() {
            const sidebar = document.querySelector('.sidebar');
            if(window.innerWidth <= 768) {
                sidebar.classList.remove('show');
            }
        });
    });
});