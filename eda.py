#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt





class EDA:
    
    def __init__(self,a): 
        self.accepted =a
        
           
    def cleanData(self):
        absent = round(100*(self.accepted.isnull().sum()/len(self.accepted.id)), 2)
        self.accepted = self.accepted.drop(list(absent[absent >= 50].index),axis=1)
        return self.accepted
    
    def plot1(self,df):
        status=df.groupby('loan_status').loan_amnt.count().sort_values(ascending=False)

        plt.figure(figsize=(6,6))
        sns.set_theme(style="whitegrid")
        ax=sns.barplot(x=status.iloc[0:3].index,y=((status.iloc[0:3].values)/1000))
        ax.bar_label(ax.containers[0])
        plt.xticks(rotation=90)
        plt.ylabel("Total Loan Amount(x10$^3$)", fontsize=12)
        plt.xlabel("Status of Loan", fontsize=12)
        plt.title("Total Loan Amount vs Status of Loan",fontweight="bold", fontsize=16)
        plt.show()
        print("Percentage of loans that are fully paid=","%.2f" % (df.loc[df['loan_status'] == 
        'Fully Paid'].loan_status.count() * 100/len(df)),'%')
        print("Percentage of loans that are current=","%.2f" % (df.loc[df['loan_status'] == 
        'Current'].loan_status.count() * 100/len(df)),'%')
        print("Percentage of loans that are charged off=","%.2f" % (df.loc[df['loan_status'] == 
        'Charged Off'].loan_status.count() * 100/len(df)),'%')

    def plot2(self,df):
        total_payment=df.groupby('loan_status'
        ).total_pymnt.sum() * 100 / df.groupby('loan_status').loan_amnt.sum().sort_values(ascending=False)

        total_payment=total_payment.sort_values(ascending=False)
        plt.figure(figsize=(8,8))
        plt.grid(color='gray', linestyle='dashed')
        ax=sns.barplot(x=total_payment.iloc[0:5].index,y=total_payment.iloc[0:5].values, palette = 'pastel')
        ax.bar_label(ax.containers[0],padding=1)
        plt.xticks(rotation=90)
        plt.ylabel('% of Payment Received for total funded amount', fontsize=12)
        plt.xlabel('Status of Loan', fontsize=12)
        plt.title('% of Payment Received for total funded amount  vs Status of Loan',fontweight="bold", fontsize=16)
        plt.show()
        
        
    def plot3(self,df):
        # first subplot on the left 
        plt.figure(figsize=(12,8))

        plt.subplot(121)
        loan_grade= df.groupby('grade').loan_amnt.count()
        plt.pie(loan_grade.values, labels =loan_grade.index , colors = sns.color_palette('pastel')[0:5], autopct='%.1f')
        plt.title('Percentage of loans per Grade',fontweight="bold", fontsize=16)

        # second subplot on the right
        plt.subplot(122)
        sns.barplot(x='grade', y='int_rate', data=df, palette = "Set2", order=['A','B','C','D','E','F','G'])
        plt.ylabel('Interest rate(%)', fontsize=10)
        plt.xlabel('Grade', fontsize=10)
        plt.title('Interest rate(%) vs Grade',fontweight="bold", fontsize=16)
        ax = plt.gca()
        for p in ax.patches:
            ax.text(p.get_x() + p.get_width()/2., p.get_height(), '{0:.2f}'.format(p.get_height()), 
                fontsize=10, color='black', ha='center', va='bottom')

        plt.tight_layout(pad=4,h_pad=4, w_pad=10)
        plt.show()
    
    
    def plot4(self,df):
        plt.figure(figsize=(16,8))
        k=sorted(df.addr_state.astype(str).unique())
        ax=sns.countplot(df['addr_state'],order=df.addr_state.value_counts().iloc[:15].index, palette="pastel")
        ax.bar_label(ax.containers[0],padding=1)
        plt.ylabel('Count of loans taken', fontsize=12)
        plt.xlabel('State', fontsize=12)
        plt.title('Top 15 states that took maximum loans',fontweight="bold", fontsize=16)
        plt.show()

        
    def plot5(self,df):
        plt.figure(figsize=(14,6))

        plt.subplot(1, 2, 1)
        c=sns.countplot(df['pub_rec'].sort_values(ascending=False),palette="Set3")
        c.set_yscale('log')
        plt.xticks(rotation=90)
        plt.ylabel('Count', fontsize=12)
        plt.xlabel('Public derogatory records', fontsize=12)
        plt.title('Total count of Derogatory Records ',fontweight="bold", fontsize=16)

        plt.subplot(1, 2, 2)
        grp = df.groupby(['loan_status', 'pub_rec'])[ 'pub_rec'].count()
        ct = df.groupby( 'pub_rec')['pub_rec'].count()
        percentages = grp.unstack() * 100 / ct.T
        loanstatus='Charged Off'
        ax = percentages.loc[loanstatus].plot.bar(color=sns.color_palette('husl', 16))
        plt.ylabel('% of Charged off Loans', fontsize=12)
        plt.xlabel('Public derogatory records', fontsize=12)
        plt.title('% of Charged off Loans vs. Number of Derogatory Records ',fontweight="bold", fontsize=16)
        plt.margins(0.2, 0.2)
        plt.tight_layout()
        plt.show()
        
        print("Percentage of customers with no derogatory records=",round(df.loc[df['pub_rec'] == 0.0].pub_rec.count() * 100/len(df),2),'%')
        print("Percentage of customers with one derogatory record=", round(float(df.loc[df['pub_rec'] == 1.0
        ].pub_rec.count()) *100/ float(len(df)),2),'%')
        print("Percentage of customers with two derogatory records=", round(float(df.loc[df['pub_rec'] == 2.0
        ].pub_rec.count()) *100/ float(len(df)),2),'%')
    
    
    def plot6(self,df):
        #defaults
        fig, axes = plt.subplots(2, 2, figsize=(22,18))
        fig.suptitle('Defaults', fontsize=18,fontweight="bold")

        #Plot 1: Defaults by Interest Rate
        sns.barplot(ax=axes[0, 0], data=df, x='chargeoff_within_12_mths', y='int_rate',ci = None )
        axes[0, 0].set_title('Defaults by interest rate',fontweight="bold", fontsize=16)
        axes[0, 0].set_xlabel('Number of charge-offs', fontsize=14)
        axes[0, 0].set_ylabel('Interest Rate', fontsize=14)

        #Plot 2: Defaults by Funded Amount
        sns.barplot(ax=axes[0, 1], data=df, x='chargeoff_within_12_mths', y='funded_amnt',ci = None )
        axes[0, 1].set_title('Defaults by Funded Amount',fontweight="bold", fontsize=16)
        axes[0, 1].set_xlabel('Number of charge-offs', fontsize=14)
        axes[0, 1].set_ylabel('Funded Amount', fontsize=14)

        #Plot 3: Defaults by Purpose
        sns.barplot(ax=axes[1, 0], data=df, x='chargeoff_within_12_mths', y='purpose',ci = None )
        axes[1, 0].set_title('Defaults by Purpose',fontweight="bold", fontsize=16)
        axes[1, 0].set_xlabel('Number of charge-offs', fontsize=14)
        axes[1, 0].set_ylabel('Purpose', fontsize=14)

        #Plot 4: Defaults by Debt to Income Ratio
        sns.barplot(ax=axes[1, 1], data=df, x='chargeoff_within_12_mths', y='dti',ci = None )
        axes[1, 1].set_title('Defaults by Debt to Income Ratio',fontweight="bold", fontsize=16)
        axes[1, 1].set_xlabel('Number of charge-offs', fontsize=14)
        axes[1, 1].set_ylabel('Debt to Income Ratio', fontsize=14)


        plt.show()


    def plot7(self,df):
        fig, axes = plt.subplots(1, 2, figsize=(20, 8))
        fig.suptitle('FICO Range(Low) Plots',fontweight="bold", fontsize=16)
        
        #Plot 1: FICO Range(low) vs Grade
        sns.boxplot(y=df['fico_range_low'], x=df['grade'].sort_values(), data=df, showfliers = False,ax=axes[0])
        axes[0].set_title('FICO Range(low) vs Grade',fontweight="bold", fontsize=14)
        axes[0].set_xlabel('Grade', fontsize=12)
        axes[0].set_ylabel('FICO Range(low)', fontsize=12)

        #Plot 2: FICO Range(low) vs Defaults
        sns.boxplot(y=df['fico_range_low'], x=df['chargeoff_within_12_mths'].sort_values(), data=df
        , showfliers = False,ax=axes[1])
        axes[1].set_title('FICO Range(low) vs Defaults',fontweight="bold", fontsize=14)
        axes[1].set_xlabel('Number of charge-offs', fontsize=12)
        axes[1].set_ylabel('FICO Range(low)', fontsize=12)
        plt.show()

    def plot8(self,df):
        fig, axes = plt.subplots(1, 2, figsize=(20, 8))
        fig.suptitle('FICO Range(Low) Plots',fontweight="bold", fontsize=16)

        #Plot 1: FICO Range(high) vs Grade
        sns.boxplot(y=df['fico_range_high'], x=df['grade'].sort_values(), data=df, showfliers = False,ax=axes[0])
        axes[0].set_title('FICO Range(high) vs Grade',fontweight="bold", fontsize=14)
        axes[0].set_xlabel('Grade', fontsize=12)
        axes[0].set_ylabel('FICO Range(high)', fontsize=12)

        #Plot 2: FICO Range(high) vs Defaults
        sns.boxplot(y=df['fico_range_high'], x=df['chargeoff_within_12_mths'].sort_values(), data=df
        , showfliers = False,ax=axes[1])
        axes[1].set_title('FICO Range(high) vs Defaults',fontweight="bold", fontsize=14)
        axes[1].set_xlabel('Number of charge-offs', fontsize=12)
        axes[1].set_ylabel('FICO Range(high)', fontsize=12)
        plt.show()
        
    def plot9(self,df):
        plt.figure(figsize=(20,9))
        sns.barplot(x='delinq_2yrs', y='loan_amnt', hue='grade',data=df
        , estimator=np.mean,order=df.delinq_2yrs.value_counts().iloc[:10].index ,ci = None )
        plt.xlabel('Number of delinquencies', fontsize=12)
        plt.ylabel('Loan Amount', fontsize=12)
        plt.title('Loan Amount vs Number of delinquencies',fontweight="bold", fontsize=16)
        plt.show()
        
    def plot10(self,df):
        fig, axes = plt.subplots(1, 2, figsize=(15,6))
        fig.suptitle('Debt to Income Ratio Plots',fontsize=16)

        #Plot 1: Count vs DTI
        sns.histplot(df['dti'],ax=axes[0],color='purple')
        axes[0].set_xlim(0,80)
        axes[0].set_title('Count vs DTI', fontsize = 14)
        axes[0].set_xlabel('DTI', fontsize = 12)
        axes[0].set_ylabel('Count', fontsize = 12)

        #Plot 2: DTI vs Grade
        sns.boxplot(y=df['dti'], x=df['grade'].sort_values(), data=df, showfliers = False,ax=axes[1], palette="Set2")
        axes[1].set_title('DTI vs Grade', fontsize = 14)
        axes[1].set_xlabel('Grade', fontsize = 12)
        axes[1].set_ylabel('DTI', fontsize = 12)
        plt.show()




