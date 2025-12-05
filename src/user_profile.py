"""
User Profile Module
Handles collection and validation of user information from forms
"""

import streamlit as st
from typing import Dict, Any, Optional

class UserProfile:
    """Manage user information from form input"""
    
    def __init__(self):
        """Initialize empty profile"""
        self.basic_info = {}
        self.financial_info = {}
        self.experience_goals = {}
        self.self_assessment = {}
        
    def collect_basic_info(self) -> Dict[str, Any]:
        """Render and collect basic information"""
        st.subheader("📝 Basic Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input(
                "Customer Name *",
                placeholder="Enter your name",
                key="user_name"
            )
            
            age = st.number_input(
                "Age *",
                min_value=18,
                max_value=100,
                value=35,
                step=1,
                key="user_age"
            )
        
        with col2:
            gender = st.selectbox(
                "Gender *",
                options=["Male", "Female", "Other"],
                key="user_gender"
            )
            
            education = st.selectbox(
                "Education *",
                options=["High School", "College", "University", "Postgraduate"],
                key="user_education"
            )
        
        self.basic_info = {
            "name": name,
            "age": age,
            "gender": gender,
            "education": education
        }
        
        return self.basic_info
    
    def collect_financial_info(self) -> Dict[str, Any]:
        """Render and collect financial information"""
        st.subheader("💰 Financial Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            income = st.selectbox(
                "Annual Income (USD) *",
                options=[
                    "< $10,000",
                    "$10,000 - $50,000",
                    "$50,000 - $100,000",
                    "> $100,000"
                ],
                key="user_income"
            )
        
        with col2:
            capital = st.number_input(
                "Trading Capital (USD) *",
                min_value=100,
                max_value=1000000,
                value=5000,
                step=100,
                key="user_capital"
            )
        
        self.financial_info = {
            "income": income,
            "capital": capital
        }
        
        return self.financial_info
    
    def collect_experience_goals(self) -> Dict[str, Any]:
        """Render and collect experience and goals"""
        st.subheader("📊 Experience & Goals")
        
        col1, col2 = st.columns(2)
        
        with col1:
            experience = st.selectbox(
                "Trading Experience *",
                options=[
                    "< 6 months",
                    "6 months - 1 year",
                    "1 - 3 years",
                    "> 3 years"
                ],
                key="user_experience"
            )
        
        with col2:
            goals = st.multiselect(
                "Investment Goals *",
                options=[
                    "Steady Income",
                    "Fast Capital Growth",
                    "Capital Preservation",
                    "Learning & Experimentation",
                    "Entertainment"
                ],
                default=["Steady Income"],
                key="user_goals"
            )
        
        self.experience_goals = {
            "experience": experience,
            "goals": goals
        }
        
        return self.experience_goals
    
    def collect_self_assessment(self) -> Dict[str, Any]:
        """Render and collect self-assessment"""
        st.subheader("🎯 Self Assessment")
        
        risk_tolerance = st.slider(
            "Risk Tolerance Level (1 = Very Conservative, 10 = Very Aggressive) *",
            min_value=1,
            max_value=10,
            value=5,
            key="user_risk"
        )
        
        available_time = st.selectbox(
            "Daily Market Monitoring Time *",
            options=[
                "< 1 hour",
                "1 - 3 hours",
                "3 - 6 hours",
                "> 6 hours"
            ],
            key="user_time"
        )
        
        self.self_assessment = {
            "risk_tolerance": risk_tolerance,
            "available_time": available_time
        }
        
        return self.self_assessment
    
    def validate_profile(self, profile_data: Optional[Dict[str, Any]] = None) -> bool:
        """Validate all required fields are filled"""
        if profile_data is None:
            profile = {
                **self.basic_info,
                **self.financial_info,
                **self.experience_goals,
                **self.self_assessment
            }
        else:
            profile = profile_data
        
        if not profile.get("name"):
            return False
        
        if not profile.get("capital"):
            return False
        
        if not profile.get("goals"):
            return False
        
        return True
    
    def get_profile_dict(self) -> Dict[str, Any]:
        """Return complete profile as dictionary"""
        return {
            **self.basic_info,
            **self.financial_info,
            **self.experience_goals,
            **self.self_assessment
        }
    
    def calculate_profile_features(self, profile_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Convert profile to features for classification
        
        Args:
            profile_data: Optional profile dictionary. If None, uses self.get_profile_dict()
        """
        if profile_data is None:
            profile = self.get_profile_dict()
        else:
            profile = profile_data
        
        # Capital level
        capital = profile.get("capital", 0)
        if capital < 5000:
            capital_level = "Small"
        elif capital < 50000:
            capital_level = "Medium"
        else:
            capital_level = "Large"
        
        # Age group
        age = profile.get("age", 35)
        if age < 25:
            age_group = "Young"
        elif age < 35:
            age_group = "Young-Adult"
        elif age < 50:
            age_group = "Middle-Aged"
        else:
            age_group = "Senior"
        
        # Experience level
        exp = profile.get("experience", "")
        if "< 6" in exp:
            experience_level = "Newbie"
        elif "6 months - 1" in exp or "6 tháng - 1" in exp:
            experience_level = "Beginner"
        elif "1 - 3" in exp:
            experience_level = "Intermediate"
        else:
            experience_level = "Experienced"
        
        # Risk appetite
        risk = profile.get("risk_tolerance", 5)
        if risk <= 3:
            risk_appetite = "Conservative"
        elif risk <= 7:
            risk_appetite = "Moderate"
        else:
            risk_appetite = "Aggressive"
        
        # Time commitment
        time = profile.get("available_time", "")
        if "< 1" in time:
            time_commitment = "Very Low"
        elif "1 - 3" in time:
            time_commitment = "Low"
        elif "3 - 6" in time:
            time_commitment = "Medium"
        else:
            time_commitment = "High"
        
        # Education level
        edu = profile.get("education", "")
        education_score = {
            "High School": 1,
            "Phổ thông": 1,
            "College": 2,
            "Trung cấp": 2,
            "University": 3,
            "Đại học": 3,
            "Postgraduate": 4,
            "Sau đại học": 4
        }.get(edu, 2)
        
        return {
            "capital_level": capital_level,
            "age_group": age_group,
            "experience_level": experience_level,
            "risk_appetite": risk_appetite,
            "time_commitment": time_commitment,
            "education_level": education_score,
            "gender": profile.get("gender", "Male"),
            "goals": profile.get("goals", [])
        }
