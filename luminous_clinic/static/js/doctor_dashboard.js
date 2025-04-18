// luminous_clinic_project/luminous_clinic/static/js/doctor_dashboard.js

document.addEventListener('DOMContentLoaded', function() {
    loadContent('home');
});

function loadContent(section) {
    const contentDiv = document.getElementById('main-content');
    switch (section) {
        case 'home':
            contentDiv.innerHTML = `
                <h1>Home</h1>
                <p>Welcome to your doctor dashboard!</p>
                <div class="summary-widgets">
                    <div class="widget">
                        <h2>Pending Requests</h2>
                        <p>{{ bookings.filter(status='Pending').count }}</p>
                    </div>
                    <div class="widget">
                        <h2>Active Consultations</h2>
                        <p>{{ bookings.filter(status='Accepted').count }}</p>
                    </div>
                    <div class="widget">
                        <h2>Completed Consultations</h2>
                        <p>{{ bookings.filter(status='Completed').count }}</p>
                    </div>
                </div>
                <button class="quick-action">Quick Action</button>
            `;
            break;
        case 'consultation-requests':
            contentDiv.innerHTML = `
                <h1>Consultation Requests</h1>
                <ul>
                    {% for booking in bookings %}
                        {% if booking.status == 'Pending' %}
                            <li>
                                <strong>{{ booking.patient.full_name }}</strong> - {{ booking.timestamp|date:"d M. Y" }}
                                <button onclick="acceptBooking({{ booking.id }})">Accept</button>
                                <button onclick="rejectBooking({{ booking.id }})">Reject</button>
                            </li>
                        {% endif %}
                    {% endfor %}
                </ul>
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
                                    <button>View Details</button>
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
                <h2>Approval Status</h2>
                <p>{% if user.doctor_profile.approved %}Approved{% else %}Pending{% endif %}</p>
                <h2>View Schedule</h2>
                <button onclick="viewSchedule()">View Schedule</button>
            `;
            break;
    }
}

function acceptBooking(bookingId) {
    fetch(`/accept-booking/${bookingId}/`, {
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
            alert('Failed to accept booking');
        }
    });
}

function rejectBooking(bookingId) {
    const reason = prompt('Enter reason for rejection:');
    if (reason) {
        fetch(`/reject-booking/${bookingId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}'
            },
            body: JSON.stringify({ reason: reason })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.reload();
            } else {
                alert('Failed to reject booking');
            }
        });
    }
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
            window.location.href = '{% url "doctor_dashboard" %}';
        } else {
            alert('Failed to end service');
        }
    });
}

function viewSchedule() {
    alert('Viewing schedule...');
}

function editNote(noteId) {
    alert('Editing note ' + noteId);
}

function deleteNote(noteId) {
    alert('Deleting note ' + noteId);
}