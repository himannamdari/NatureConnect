def calculate_biophilia_score(answers):
    """
    Calculate a biophilia score based on quiz answers
    
    Parameters:
    - answers: list of integer answers from 1-10
    
    Returns:
    - integer score from 0-100
    """
    # Simple calculation - sum of answers normalized to 0-100
    if not answers:
        return 0
    
    # Sum all answers
    total = sum(answers)
    
    # Maximum possible score (10 points per question)
    max_score = len(answers) * 10
    
    # Calculate percentage and round to nearest integer
    score = round((total / max_score) * 100)
    
    return score

def get_biophilia_recommendations(score, user_location=None):
    """
    Get personalized recommendations based on biophilia score
    
    Parameters:
    - score: integer biophilia score from 0-100
    - user_location: optional location for localized recommendations
    
    Returns:
    - dictionary of recommendations
    """
    # Default recommendations
    recommendations = {
        'activities': [],
        'resources': [],
        'daily_practices': []
    }
    
    # Low connection to nature (0-40)
    if score < 40:
        recommendations['activities'] = [
            'Visit a local park for 15 minutes daily',
            'Start a small indoor plant collection',
            'Watch nature documentaries',
            'Take a guided nature walk'
        ]
        recommendations['resources'] = [
            'Book: "The Nature Fix" by Florence Williams',
            'App: "iNaturalist" for identifying plants and animals',
            'Website: AllTrails.com for finding nearby nature spots'
        ]
        recommendations['daily_practices'] = [
            'Take breaks to look at the sky and clouds',
            'Listen to nature sounds while working',
            'Eat lunch outdoors when possible',
            'Notice wildlife in your neighborhood'
        ]
    
    # Moderate connection to nature (40-70)
    elif score < 70:
        recommendations['activities'] = [
            'Try forest bathing (mindful nature immersion)',
            'Start a small garden (even container gardening counts)',
            'Join a local conservation volunteer group',
            'Take up nature photography or sketching'
        ]
        recommendations['resources'] = [
            'Book: "Braiding Sweetgrass" by Robin Wall Kimmerer',
            'App: "Seek" by iNaturalist for nature challenges',
            'Podcast: "For the Wild" on ecological restoration'
        ]
        recommendations['daily_practices'] = [
            'Establish a "sit spot" for regular nature observation',
            'Incorporate natural materials in your home',
            'Practice identifying bird calls and songs',
            'Track moon phases and seasonal changes'
        ]
    
    # Strong connection to nature (70-100)
    else:
        recommendations['activities'] = [
            'Participate in citizen science projects',
            'Lead nature walks for others',
            'Create a certified wildlife habitat in your yard',
            'Try solo wilderness experiences'
        ]
        recommendations['resources'] = [
            'Book: "The Hidden Life of Trees" by Peter Wohlleben',
            'Organization: Join your local native plant society',
            'Course: Wilderness first aid certification'
        ]
        recommendations['daily_practices'] = [
            'Mentor others in nature connection',
            'Keep a detailed nature journal',
            'Practice traditional skills (foraging, tracking)',
            'Create rituals celebrating seasonal changes'
        ]
    
    # Add user-specific recommendations if location is provided
    if user_location:
        recommendations['location_based'] = [
            'Custom recommendations would be generated based on user location',
            'This would include local trails, parks, and nature events'
        ]
    
    return recommendations
