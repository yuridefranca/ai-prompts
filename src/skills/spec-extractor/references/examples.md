# Examples: Good vs Poor Requirements

## Requirements

### Good Requirement

✅ REQ-1: User can upload profile image in JPG/PNG format, max 5MB, which is resized to 512x512px and stored in S3

**Why it's good**:
- Specific file formats (JPG/PNG)
- Clear size limit (5MB)
- Defined output (512x512px)
- Clear destination (S3)

### Poor Requirement

❌ REQ-1: User can upload profile picture

**Why it's poor**:
- No file format specified
- No size limits
- No processing details
- No storage location

## Edge Cases

### Good Edge Case

✅ EDGE-1: User uploads 10MB image → Return 400 error: "Image must be under 5MB"

**Why it's good**:
- Specific scenario (10MB image)
- Clear response (400 error)
- Helpful error message

### Poor Edge Case

❌ EDGE-1: User uploads large image → Show error

**Why it's poor**:
- "Large" is ambiguous
- No HTTP status code
- No specific error message

## Acceptance Criteria

### Good Acceptance Criterion

✅ AC-1: Given a logged-in user with no profile image, When they upload a 3MB PNG file, Then the image is resized to 512x512px, stored in S3, and profile page displays the image within 2 seconds

**Why it's good**:
- Clear precondition (logged-in, no existing image)
- Specific action (3MB PNG)
- Measurable outcome (512x512px, S3, 2 seconds)
- Testable (can automate verification)

### Poor Acceptance Criterion

❌ AC-1: User can upload image and see it on their profile

**Why it's poor**:
- No preconditions specified
- Vague action (any image?)
- No measurable outcome
- Hard to test objectively
