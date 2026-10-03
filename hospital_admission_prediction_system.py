"""
Hospital Admission Prediction System
Predicts hospital admission requirements using patient health data and ML
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, roc_curve, auc
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10

def generate_patient_dataset(n_samples=3000, admission_rate=0.35, random_state=42):
    """Generate synthetic patient dataset with admission labels"""
    np.random.seed(random_state)
    
    data = []
    n_admitted = int(n_samples * admission_rate)
    n_not_admitted = n_samples - n_admitted
    
    # Patients not requiring admission
    for i in range(n_not_admitted):
        age = np.random.normal(loc=45, scale=20)
        age = max(18, min(100, age))
        
        fever = np.random.choice([0, 1], p=[0.9, 0.1])
        cough = np.random.choice([0, 1], p=[0.85, 0.15])
        shortness_of_breath = np.random.choice([0, 1], p=[0.95, 0.05])
        chest_pain = np.random.choice([0, 1], p=[0.92, 0.08])
        
        blood_pressure_systolic = np.random.normal(loc=120, scale=15)
        blood_pressure_diastolic = np.random.normal(loc=80, scale=10)
        heart_rate = np.random.normal(loc=75, scale=10)
        oxygen_saturation = np.random.normal(loc=97, scale=2)
        
        diabetes = np.random.choice([0, 1], p=[0.85, 0.15])
        hypertension = np.random.choice([0, 1], p=[0.80, 0.20])
        heart_disease = np.random.choice([0, 1], p=[0.92, 0.08])
        
        data.append({
            'Patient_ID': f'P{i:05d}',
            'Age': age,
            'Fever': fever,
            'Cough': cough,
            'Shortness_of_Breath': shortness_of_breath,
            'Chest_Pain': chest_pain,
            'BP_Systolic': blood_pressure_systolic,
            'BP_Diastolic': blood_pressure_diastolic,
            'Heart_Rate': heart_rate,
            'Oxygen_Saturation': oxygen_saturation,
            'Diabetes': diabetes,
            'Hypertension': hypertension,
            'Heart_Disease': heart_disease,
            'Admission': 0
        })
    
    # Patients requiring admission
    for i in range(n_admitted):
        age = np.random.normal(loc=65, scale=18)
        age = max(18, min(100, age))
        
        fever = np.random.choice([0, 1], p=[0.4, 0.6])
        cough = np.random.choice([0, 1], p=[0.3, 0.7])
        shortness_of_breath = np.random.choice([0, 1], p=[0.2, 0.8])
        chest_pain = np.random.choice([0, 1], p=[0.3, 0.7])
        
        blood_pressure_systolic = np.random.normal(loc=145, scale=20)
        blood_pressure_diastolic = np.random.normal(loc=95, scale=15)
        heart_rate = np.random.normal(loc=95, scale=15)
        oxygen_saturation = np.random.normal(loc=92, scale=4)
        
        diabetes = np.random.choice([0, 1], p=[0.4, 0.6])
        hypertension = np.random.choice([0, 1], p=[0.3, 0.7])
        heart_disease = np.random.choice([0, 1], p=[0.5, 0.5])
        
        data.append({
            'Patient_ID': f'P{n_not_admitted+i:05d}',
            'Age': age,
            'Fever': fever,
            'Cough': cough,
            'Shortness_of_Breath': shortness_of_breath,
            'Chest_Pain': chest_pain,
            'BP_Systolic': blood_pressure_systolic,
            'BP_Diastolic': blood_pressure_diastolic,
            'Heart_Rate': heart_rate,
            'Oxygen_Saturation': oxygen_saturation,
            'Diabetes': diabetes,
            'Hypertension': hypertension,
            'Heart_Disease': heart_disease,
            'Admission': 1
        })
    
    df = pd.DataFrame(data)
    df = df.sample(frac=1, random_state=random_state).reset_index(drop=True)
    return df

def prepare_features(df):
    """Prepare features for modeling"""
    df_copy = df.copy()
    
    # Select features
    feature_cols = ['Age', 'Fever', 'Cough', 'Shortness_of_Breath', 'Chest_Pain',
                   'BP_Systolic', 'BP_Diastolic', 'Heart_Rate', 'Oxygen_Saturation',
                   'Diabetes', 'Hypertension', 'Heart_Disease']
    
    X = df_copy[feature_cols]
    y = df_copy['Admission']
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_scaled = pd.DataFrame(X_scaled, columns=feature_cols)
    
    return X_scaled, y, scaler

def train_models(X_train, X_test, y_train, y_test):
    """Train multiple admission prediction models"""
    models = {}
    results = []
    predictions = {}
    
    # Logistic Regression
    print("Training Logistic Regression...")
    lr = LogisticRegression(max_iter=1000, random_state=42)
    lr.fit(X_train, y_train)
    y_pred_lr = lr.predict(X_test)
    y_pred_proba_lr = lr.predict_proba(X_test)[:, 1]
    
    models['Logistic Regression'] = lr
    predictions['Logistic Regression'] = (y_pred_lr, y_pred_proba_lr)
    results.append({
        'Model': 'Logistic Regression',
        'Accuracy': accuracy_score(y_test, y_pred_lr),
        'Precision': precision_score(y_test, y_pred_lr),
        'Recall': recall_score(y_test, y_pred_lr),
        'F1_Score': f1_score(y_test, y_pred_lr),
        'ROC_AUC': roc_auc_score(y_test, y_pred_proba_lr)
    })
    
    # Random Forest
    print("Training Random Forest...")
    rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)
    y_pred_rf = rf.predict(X_test)
    y_pred_proba_rf = rf.predict_proba(X_test)[:, 1]
    
    models['Random Forest'] = rf
    predictions['Random Forest'] = (y_pred_rf, y_pred_proba_rf)
    results.append({
        'Model': 'Random Forest',
        'Accuracy': accuracy_score(y_test, y_pred_rf),
        'Precision': precision_score(y_test, y_pred_rf),
        'Recall': recall_score(y_test, y_pred_rf),
        'F1_Score': f1_score(y_test, y_pred_rf),
        'ROC_AUC': roc_auc_score(y_test, y_pred_proba_rf)
    })
    
    # Gradient Boosting
    print("Training Gradient Boosting...")
    gb = GradientBoostingClassifier(n_estimators=100, random_state=42)
    gb.fit(X_train, y_train)
    y_pred_gb = gb.predict(X_test)
    y_pred_proba_gb = gb.predict_proba(X_test)[:, 1]
    
    models['Gradient Boosting'] = gb
    predictions['Gradient Boosting'] = (y_pred_gb, y_pred_proba_gb)
    results.append({
        'Model': 'Gradient Boosting',
        'Accuracy': accuracy_score(y_test, y_pred_gb),
        'Precision': precision_score(y_test, y_pred_gb),
        'Recall': recall_score(y_test, y_pred_gb),
        'F1_Score': f1_score(y_test, y_pred_gb),
        'ROC_AUC': roc_auc_score(y_test, y_pred_proba_gb)
    })
    
    return models, pd.DataFrame(results), predictions, y_test

def plot_admission_distribution(df):
    """Plot admission distribution"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    admission_counts = df['Admission'].value_counts()
    colors = ['#2ecc71', '#e74c3c']
    
    axes[0].bar(['Not Admitted', 'Admitted'], [admission_counts[0], admission_counts[1]], 
               color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    axes[0].set_ylabel('Count', fontsize=11, fontweight='bold')
    axes[0].set_title('Patient Admission Distribution', fontsize=12, fontweight='bold')
    axes[0].grid(axis='y', alpha=0.3)
    for i, v in enumerate([admission_counts[0], admission_counts[1]]):
        axes[0].text(i, v + 20, str(v), ha='center', fontweight='bold')
    
    # Pie chart
    axes[1].pie([admission_counts[0], admission_counts[1]], labels=['Not Admitted', 'Admitted'],
               colors=colors, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 11, 'weight': 'bold'})
    axes[1].set_title('Admission Rate Distribution', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/admission_distribution.png', dpi=300, bbox_inches='tight')
    print("Saved: admission_distribution.png")
    plt.close()

def plot_model_comparison(results_df):
    """Plot model performance comparison"""
    fig, axes = plt.subplots(2, 3, figsize=(14, 8))
    
    colors = ['#3498db', '#e74c3c', '#2ecc71']
    metrics = ['Accuracy', 'Precision', 'Recall', 'F1_Score', 'ROC_AUC']
    
    for idx, metric in enumerate(metrics):
        row = idx // 3
        col = idx % 3
        
        axes[row, col].bar(results_df['Model'], results_df[metric], color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
        axes[row, col].set_ylabel(metric, fontsize=11, fontweight='bold')
        axes[row, col].set_title(f'{metric} Comparison', fontsize=12, fontweight='bold')
        axes[row, col].set_ylim([0, 1.1])
        axes[row, col].grid(axis='y', alpha=0.3)
        axes[row, col].tick_params(axis='x', rotation=45)
        
        for i, v in enumerate(results_df[metric]):
            axes[row, col].text(i, v + 0.02, f'{v:.3f}', ha='center', fontweight='bold', fontsize=9)
    
    # Remove extra subplot
    fig.delaxes(axes[1, 2])
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/admission_model_comparison.png', dpi=300, bbox_inches='tight')
    print("Saved: admission_model_comparison.png")
    plt.close()

def plot_confusion_matrices(models, predictions, y_test):
    """Plot confusion matrices for all models"""
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    
    for idx, (model_name, (y_pred, _)) in enumerate(predictions.items()):
        cm = confusion_matrix(y_test, y_pred)
        
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[idx], 
                   cbar_kws={'label': 'Count'}, annot_kws={'fontsize': 12, 'weight': 'bold'})
        axes[idx].set_xlabel('Predicted', fontsize=11, fontweight='bold')
        axes[idx].set_ylabel('Actual', fontsize=11, fontweight='bold')
        axes[idx].set_title(f'{model_name}', fontsize=12, fontweight='bold')
        axes[idx].set_xticklabels(['Not Admitted', 'Admitted'])
        axes[idx].set_yticklabels(['Not Admitted', 'Admitted'])
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/admission_confusion_matrices.png', dpi=300, bbox_inches='tight')
    print("Saved: admission_confusion_matrices.png")
    plt.close()

def plot_roc_curves(models, predictions, y_test):
    """Plot ROC curves for all models"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    colors = ['#3498db', '#e74c3c', '#2ecc71']
    
    for (model_name, (_, y_pred_proba)), color in zip(predictions.items(), colors):
        fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
        roc_auc = auc(fpr, tpr)
        ax.plot(fpr, tpr, color=color, lw=2.5, label=f'{model_name} (AUC = {roc_auc:.3f})')
    
    ax.plot([0, 1], [0, 1], 'k--', lw=2, label='Random Classifier')
    ax.set_xlabel('False Positive Rate', fontsize=11, fontweight='bold')
    ax.set_ylabel('True Positive Rate', fontsize=11, fontweight='bold')
    ax.set_title('ROC Curves - Hospital Admission Prediction', fontsize=12, fontweight='bold')
    ax.legend(loc='lower right', fontsize=10)
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/admission_roc_curves.png', dpi=300, bbox_inches='tight')
    print("Saved: admission_roc_curves.png")
    plt.close()

def plot_feature_importance(models):
    """Plot feature importance"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    feature_names = ['Age', 'Fever', 'Cough', 'SOB', 'Chest Pain', 'BP Sys', 'BP Dia', 'HR', 'O2 Sat', 'Diabetes', 'HTN', 'Heart Dis']
    
    # Random Forest
    rf = models['Random Forest']
    importance_rf = pd.DataFrame({
        'Feature': feature_names,
        'Importance': rf.feature_importances_
    }).sort_values('Importance', ascending=False)
    
    axes[0].barh(importance_rf['Feature'], importance_rf['Importance'], 
                color='#3498db', alpha=0.8, edgecolor='black', linewidth=1.5)
    axes[0].set_xlabel('Importance', fontsize=11, fontweight='bold')
    axes[0].set_title('Random Forest - Feature Importance', fontsize=12, fontweight='bold')
    axes[0].invert_yaxis()
    axes[0].grid(axis='x', alpha=0.3)
    
    # Gradient Boosting
    gb = models['Gradient Boosting']
    importance_gb = pd.DataFrame({
        'Feature': feature_names,
        'Importance': gb.feature_importances_
    }).sort_values('Importance', ascending=False)
    
    axes[1].barh(importance_gb['Feature'], importance_gb['Importance'],
                color='#e74c3c', alpha=0.8, edgecolor='black', linewidth=1.5)
    axes[1].set_xlabel('Importance', fontsize=11, fontweight='bold')
    axes[1].set_title('Gradient Boosting - Feature Importance', fontsize=12, fontweight='bold')
    axes[1].invert_yaxis()
    axes[1].grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/admission_feature_importance.png', dpi=300, bbox_inches='tight')
    print("Saved: admission_feature_importance.png")
    plt.close()

def plot_clinical_analysis(df):
    """Plot clinical parameters analysis"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 8))
    
    # Age distribution
    admitted = df[df['Admission'] == 1]['Age']
    not_admitted = df[df['Admission'] == 0]['Age']
    
    axes[0, 0].hist([not_admitted, admitted], bins=20, label=['Not Admitted', 'Admitted'],
                   color=['#2ecc71', '#e74c3c'], alpha=0.7, edgecolor='black', linewidth=1.5)
    axes[0, 0].set_xlabel('Age (years)', fontsize=11, fontweight='bold')
    axes[0, 0].set_ylabel('Frequency', fontsize=11, fontweight='bold')
    axes[0, 0].set_title('Age Distribution by Admission Status', fontsize=12, fontweight='bold')
    axes[0, 0].legend()
    axes[0, 0].grid(axis='y', alpha=0.3)
    
    # Oxygen saturation
    axes[0, 1].hist([df[df['Admission'] == 0]['Oxygen_Saturation'], df[df['Admission'] == 1]['Oxygen_Saturation']], 
                   bins=15, label=['Not Admitted', 'Admitted'],
                   color=['#2ecc71', '#e74c3c'], alpha=0.7, edgecolor='black', linewidth=1.5)
    axes[0, 1].set_xlabel('Oxygen Saturation (%)', fontsize=11, fontweight='bold')
    axes[0, 1].set_ylabel('Frequency', fontsize=11, fontweight='bold')
    axes[0, 1].set_title('Oxygen Saturation by Admission Status', fontsize=12, fontweight='bold')
    axes[0, 1].legend()
    axes[0, 1].grid(axis='y', alpha=0.3)
    
    # Chronic disease prevalence
    disease_data = []
    for disease in ['Diabetes', 'Hypertension', 'Heart_Disease']:
        admitted_pct = df[df['Admission'] == 1][disease].mean() * 100
        not_admitted_pct = df[df['Admission'] == 0][disease].mean() * 100
        disease_data.append({'Disease': disease, 'Admitted': admitted_pct, 'Not Admitted': not_admitted_pct})
    
    disease_df = pd.DataFrame(disease_data)
    x = np.arange(len(disease_df))
    width = 0.35
    
    axes[1, 0].bar(x - width/2, disease_df['Not Admitted'], width, label='Not Admitted', color='#2ecc71', alpha=0.8, edgecolor='black', linewidth=1.5)
    axes[1, 0].bar(x + width/2, disease_df['Admitted'], width, label='Admitted', color='#e74c3c', alpha=0.8, edgecolor='black', linewidth=1.5)
    axes[1, 0].set_ylabel('Prevalence (%)', fontsize=11, fontweight='bold')
    axes[1, 0].set_title('Chronic Disease Prevalence by Admission Status', fontsize=12, fontweight='bold')
    axes[1, 0].set_xticks(x)
    axes[1, 0].set_xticklabels(['Diabetes', 'Hypertension', 'Heart Disease'])
    axes[1, 0].legend()
    axes[1, 0].grid(axis='y', alpha=0.3)
    
    # Symptom prevalence
    symptom_data = []
    for symptom in ['Fever', 'Cough', 'Shortness_of_Breath', 'Chest_Pain']:
        admitted_pct = df[df['Admission'] == 1][symptom].mean() * 100
        not_admitted_pct = df[df['Admission'] == 0][symptom].mean() * 100
        symptom_data.append({'Symptom': symptom, 'Admitted': admitted_pct, 'Not Admitted': not_admitted_pct})
    
    symptom_df = pd.DataFrame(symptom_data)
    x = np.arange(len(symptom_df))
    
    axes[1, 1].bar(x - width/2, symptom_df['Not Admitted'], width, label='Not Admitted', color='#2ecc71', alpha=0.8, edgecolor='black', linewidth=1.5)
    axes[1, 1].bar(x + width/2, symptom_df['Admitted'], width, label='Admitted', color='#e74c3c', alpha=0.8, edgecolor='black', linewidth=1.5)
    axes[1, 1].set_ylabel('Prevalence (%)', fontsize=11, fontweight='bold')
    axes[1, 1].set_title('Symptom Prevalence by Admission Status', fontsize=12, fontweight='bold')
    axes[1, 1].set_xticks(x)
    axes[1, 1].set_xticklabels(['Fever', 'Cough', 'SOB', 'Chest Pain'], rotation=45)
    axes[1, 1].legend()
    axes[1, 1].grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/admission_clinical_analysis.png', dpi=300, bbox_inches='tight')
    print("Saved: admission_clinical_analysis.png")
    plt.close()

def main():
    print("="*80)
    print("HOSPITAL ADMISSION PREDICTION SYSTEM")
    print("="*80)
    
    # Generate dataset
    print("\n[1] Generating synthetic patient dataset...")
    df = generate_patient_dataset(n_samples=3000, admission_rate=0.35)
    df.to_csv('/home/ubuntu/hospital_admission_data.csv', index=False)
    print(f"Dataset generated: {len(df)} patients")
    print(f"Admission cases: {df['Admission'].sum()} ({df['Admission'].mean()*100:.2f}%)")
    
    # Prepare features
    print("\n[2] Preparing features...")
    X, y, scaler = prepare_features(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"Training set: {len(X_train)}, Test set: {len(X_test)}")
    
    # Train models
    print("\n[3] Training admission prediction models...")
    models, results_df, predictions, y_test = train_models(X_train, X_test, y_train, y_test)
    results_df.to_csv('/home/ubuntu/admission_model_results.csv', index=False)
    print("\nModel Results:")
    print(results_df.to_string(index=False))
    
    # Generate visualizations
    print("\n[4] Generating visualizations...")
    plot_admission_distribution(df)
    plot_model_comparison(results_df)
    plot_confusion_matrices(models, predictions, y_test)
    plot_roc_curves(models, predictions, y_test)
    plot_feature_importance(models)
    plot_clinical_analysis(df)
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE - All visualizations saved")
    print("="*80)

if __name__ == "__main__":
    main()
