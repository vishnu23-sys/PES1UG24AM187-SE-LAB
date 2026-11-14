# Lab 3: Architecture and Component Diagram

Architecture design for **Problem 6**, the Alumni Mentorship & Mock Interview Platform.

## What I did

- **Chose a Client-Server architecture** and explained why Layered and Microservices fit worse:
  - one server owns the availability calendar, so a slot is booked in a single atomic transaction and can never be double-booked (FR-003);
  - profiles and interview scorecards stay on central servers, so the rule that users only see what they are allowed to (NFR-001, FR-004) is enforced in one place.
- **Security and performance arguments:** thin clients hold no copies of private data, with TLS 1.3 in transit, AES-256 at rest and role-based access; mentor matching uses a shared in-memory index and cache on the server.
- **Component diagram** with the Student Mentee Client App, the Alumni Mentor Portal Client, the Profile & Mentor Matching Server, the Session Booking & Calendar Server and the Interview Scorecard Server, plus their interfaces (`IMentorSearch`, `IMentorAvailability`, `IAvailabilityManagement`, `ISessionBooking`, …).
- **Traceability table** mapping every FR and NFR from Lab 1 to the part of the architecture that handles it.

## Contents

- `PES1UG24AM187_LAB3_PROBLEM-6.pdf`: the submitted write-up (6 pages)
