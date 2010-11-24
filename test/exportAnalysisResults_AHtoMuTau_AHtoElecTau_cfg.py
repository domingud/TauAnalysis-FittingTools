import FWCore.ParameterSet.Config as cms

from TauAnalysis.Configuration.recoSampleDefinitionsAHtoMuTau_7TeV_grid_cfi import *

#--------------------------------------------------------------------------------
# Export analysis results into ASCII files,
# in the format used by the CDF collaboration
#--------------------------------------------------------------------------------

process = cms.Process('exportAnalysisResults')

process.DQMStore = cms.Service("DQMStore")

process.maxEvents = cms.untracked.PSet(            
    input = cms.untracked.int32(0)         
)

process.source = cms.Source("EmptySource")

higgsMassPoints = [ '100', '130', '160', '200', '300' ]

process.loadAnalysisResults = cms.EDAnalyzer("DQMFileLoader",
    all = cms.PSet(
        inputFileNames = cms.vstring(
            '/data1/veelken/CMSSW_3_8_x/plots/MSSM_Higgs_combined/plotsAHtoMuTau_skimmed.root',
            '/data1/veelken/CMSSW_3_8_x/plots/MSSM_Higgs_combined/plotsZtoElecTau_skimmed.root'
        ),
        dqmDirectory_store = cms.string('/export')
    )
)

process.dumpDQMStore = cms.EDAnalyzer("DQMStoreDump")

process.sumAHtoElecTau = cms.EDAnalyzer("DQMHistAdder",
    qcdSum = cms.PSet(
        dqmDirectories_input = cms.vstring(
            '/export/summed/harvested/qcdBCtoESum/zElecTauAnalyzer/',
            '/export/summed/harvested/qcdEMenrichedSum/zElecTauAnalyzer/'
        ),
        dqmDirectory_output = cms.string('/export/summed/harvested/qcdSum/zElecTauAnalyzer/')
    ),
    WplusJetsSum = cms.PSet(
        dqmDirectories_input = cms.vstring(
            '/export/summed/harvested/WtoENu/zElecTauAnalyzer/',
            '/export/summed/harvested/WtoTauNu/zElecTauAnalyzer/'
        ),
        dqmDirectory_output = cms.string('/export/summed/harvested/WplusJetsSum/zElecTauAnalyzer/')
    )                                   

)

psets = []

for higgsMassPoint in higgsMassPoints:

    pset = cms.PSet(
        meName_input = cms.string(
            ('/export/harvested/A%sSum/ahMuTauAnalyzer_woBtag/FilterStatistics/' \
           + 'evtSelNonCentralJetEt20bTag/passed_cumulative_numWeighted#a1#s1') % higgsMassPoint
        ),
        meName_output = cms.string(
            ('/export/harvested/A%sSum/ahElecTauAnalyzer_prediction/FilterStatistics/' \
           + 'evtSelElecTauPairZeeHypothesisVeto/passed_cumulative_numWeighted#a1#s1') % higgsMassPoint
        ),
        meType = cms.string("real"),
        scaleFactor = cms.double(0.613)
    )

    psets.append(pset)

process.compAHtoElecTauPrediction = cms.EDAnalyzer("DQMHistScaler",
    config = cms.VPSet(psets)
)                                                   

AHtoMuTau_systematics = [
##    'muonPtUp',
##    'muonPtDown',
##    'tauJetEnUp',
##    'tauJetEnDown',
##    'jetEnUp',
##    'jetEnDown'
]

AHtoElecTau_systematics = [
##    'elecEnUp',
##    'elecEnDown',
##    'tauJetEnUp',
##    'tauJetEnDown',
##    'jetEnUp',
##    'jetEnDown'
]

dqmDirectoryTemplateAHtoMuTau = '/export/harvested/%s/ahMuTauAnalyzer_woBtag/afterEvtSelNonCentralJetEt20bTag/'
dqmDirectoryFilterStatAHtoMuTau = '/export/harvested/%s/ahMuTauAnalyzer_woBtag/FilterStatistics/'
meNameTemplateAHtoMuTau = 'DiTauCandidateSVfitQuantities/psKine_MEt_ptBalance/Mass'
meNameNumEventsProcessedAHtoMuTau = 'genPhaseSpaceCut/passed_cumulative_numWeighted#a1#s1'
meNameNumEventsPassedAHtoMuTau = 'evtSelNonCentralJetEt20bTag/passed_cumulative_numWeighted#a1#s1'

dqmDirectoryTemplateAHtoElecTau = '/export/summed/harvested/%s/zElecTauAnalyzer/afterEvtSelElecTauPairZeeHypothesisVeto/'
dqmDirectoryFilterStatAHtoElecTau = '/export/summed/harvested/%s/zElecTauAnalyzer/FilterStatistics/'
meNameTemplateAHtoElecTau = 'DiTauCandidateSVfitQuantities/psKine_MEt_ptBalance/Mass'
meNameNumEventsProcessedAHtoElecTau = 'genPhaseSpaceCut/passed_cumulative_numWeighted#a1#s1'
meNameNumEventsPassedAHtoElecTau = 'evtSelElecTauPairZeeHypothesisVeto/passed_cumulative_numWeighted#a1#s1'

process.exportAnalysisResults = cms.EDAnalyzer("DQMExportAnalysisResults",

    channels = cms.VPSet(
        cms.PSet(
            name = cms.string("AHtoMuTau"),
            shortName = cms.string("ma"),
            binning = cms.string(
                dqmDirectoryTemplateAHtoMuTau % 'Ztautau'
               + meNameTemplateAHtoMuTau
            )
        ),
        cms.PSet(
            name = cms.string("AHtoElecTau"),
            shortName = cms.string("ea"),
            binning = cms.string(
                dqmDirectoryTemplateAHtoElecTau % 'Ztautau'
               + meNameTemplateAHtoElecTau
            )
        )
    ),

    outputFilePath = cms.string("/data1/veelken/CMSSW_3_8_x/plots/MSSM_Higgs_combined/export"),                 

    processes = cms.PSet(
        Ztautau = cms.PSet(
            distributions = cms.PSet(
                AHtoMuTau = cms.PSet(
                    template = cms.string(
                        dqmDirectoryTemplateAHtoMuTau % 'Ztautau'
                       + '#SYSTEMATICSDIR#/' + meNameTemplateAHtoMuTau
                    ),
                    systematics = cms.vstring(AHtoMuTau_systematics),
                    normalization = cms.PSet(
                         numEventsProcessed = cms.string(
                             dqmDirectoryFilterStatAHtoMuTau % 'Ztautau'
                            + '#SYSTEMATICSDIR#/' + meNameNumEventsProcessedAHtoMuTau
                         ),
                         numEventsPassed = cms.string(
                             dqmDirectoryFilterStatAHtoMuTau % 'Ztautau'
                            + '#SYSTEMATICSDIR#/' + meNameNumEventsPassedAHtoMuTau
                         )
                    )
                ),        
                AHtoElecTau = cms.PSet(
                    template = cms.string(
                        dqmDirectoryTemplateAHtoElecTau % 'Ztautau'
                       + '#SYSTEMATICSDIR#/' + meNameTemplateAHtoElecTau
                    ),
                    systematics = cms.vstring(AHtoElecTau_systematics),
                    normalization = cms.PSet(
                         numEventsProcessed = cms.string(
                             dqmDirectoryFilterStatAHtoElecTau % 'Ztautau'
                            + '#SYSTEMATICSDIR#/' + meNameNumEventsProcessedAHtoElecTau
                         ),
                         numEventsPassed = cms.string(
                             dqmDirectoryFilterStatAHtoElecTau % 'Ztautau'
                            + '#SYSTEMATICSDIR#/' + meNameNumEventsPassedAHtoElecTau
                         )
                    )
                )
            ),
            outputFilePath = cms.string(""),
	    outputFileName = cms.string("ztt_#CHANNEL_OUTPUTFILENAME#.hst")
        ),
        Zee = cms.PSet(
            distributions = cms.PSet(
                AHtoElecTau = cms.PSet(
                    template = cms.string(
                        dqmDirectoryTemplateAHtoElecTau % 'Zee'
                       + '#SYSTEMATICSDIR#/' + meNameTemplateAHtoElecTau
                    ),
                    systematics = cms.vstring(AHtoElecTau_systematics),
                    normalization = cms.PSet(
                         numEventsProcessed = cms.string(
                             dqmDirectoryFilterStatAHtoElecTau % 'Zee'
                            + '#SYSTEMATICSDIR#/' + meNameNumEventsProcessedAHtoElecTau
                         ),
                         numEventsPassed = cms.string(
                             dqmDirectoryFilterStatAHtoElecTau % 'Zee'
                            + '#SYSTEMATICSDIR#/' + meNameNumEventsPassedAHtoElecTau
                         )
                    )
                )
            ),
            outputFilePath = cms.string(""),
	    outputFileName = cms.string("zee_#CHANNEL_OUTPUTFILENAME#.hst")
        ),
        Zmumu = cms.PSet(
            distributions = cms.PSet(
                AHtoMuTau = cms.PSet(
                    template = cms.string(
                        dqmDirectoryTemplateAHtoMuTau % 'Zmumu'
                       + '#SYSTEMATICSDIR#/' + meNameTemplateAHtoMuTau
                    ),
                    systematics = cms.vstring(AHtoMuTau_systematics),
                    normalization = cms.PSet(
                         numEventsProcessed = cms.string(
                             dqmDirectoryFilterStatAHtoMuTau % 'Zmumu'
                            + '#SYSTEMATICSDIR#/' + meNameNumEventsProcessedAHtoMuTau
                         ),
                         numEventsPassed = cms.string(
                             dqmDirectoryFilterStatAHtoMuTau % 'Zmumu'
                            + '#SYSTEMATICSDIR#/' + meNameNumEventsPassedAHtoMuTau
                         )
                    )
                )
            ),
            outputFilePath = cms.string(""),                                   
	    outputFileName = cms.string("zmm_#CHANNEL_OUTPUTFILENAME#.hst")
        ),                                      
        QCD = cms.PSet(
            distributions = cms.PSet(
                AHtoMuTau = cms.PSet(
                    template = cms.string(
                        dqmDirectoryTemplateAHtoMuTau % 'qcdSum'
                       + '#SYSTEMATICSDIR#/' + meNameTemplateAHtoMuTau
                    ),
                    systematics = cms.vstring(AHtoMuTau_systematics),
                    normalization = cms.PSet(
                         numEventsProcessed = cms.string(
                             dqmDirectoryFilterStatAHtoMuTau % 'qcdSum'
                            + '#SYSTEMATICSDIR#/' + meNameNumEventsProcessedAHtoMuTau
                         ),
                         numEventsPassed = cms.string(
                             dqmDirectoryFilterStatAHtoMuTau % 'qcdSum'
                            + '#SYSTEMATICSDIR#/' + meNameNumEventsPassedAHtoMuTau
                         )
                    )
                ),
                AHtoElecTau = cms.PSet(
                    template = cms.string(
                        dqmDirectoryTemplateAHtoElecTau % 'qcdSum'
                       + '#SYSTEMATICSDIR#/' + meNameTemplateAHtoElecTau
                    ),
                    systematics = cms.vstring(AHtoElecTau_systematics),
                    normalization = cms.PSet(
                         numEventsProcessed = cms.string(
                             dqmDirectoryFilterStatAHtoElecTau % 'qcdSum'
                            + '#SYSTEMATICSDIR#/' + meNameNumEventsProcessedAHtoElecTau
                         ),
                         numEventsPassed = cms.string(
                             dqmDirectoryFilterStatAHtoElecTau % 'qcdSum'
                            + '#SYSTEMATICSDIR#/' + meNameNumEventsPassedAHtoElecTau
                         )
                    )
                )
            ),
            outputFilePath = cms.string(""),
	    outputFileName = cms.string("qcd_#CHANNEL_OUTPUTFILENAME#.hst")
        ),    
        WplusJets = cms.PSet(
            distributions = cms.PSet(
                AHtoMuTau = cms.PSet(
                    template = cms.string(
                        dqmDirectoryTemplateAHtoMuTau % 'WplusJets'
                       + '#SYSTEMATICSDIR#/' + meNameTemplateAHtoMuTau
                    ),
                    systematics = cms.vstring(AHtoMuTau_systematics),
                    normalization = cms.PSet(
                         numEventsProcessed = cms.string(
                             dqmDirectoryFilterStatAHtoMuTau % 'WplusJets'
                            + '#SYSTEMATICSDIR#/' + meNameNumEventsProcessedAHtoMuTau
                         ),
                         numEventsPassed = cms.string(
                             dqmDirectoryFilterStatAHtoMuTau % 'WplusJets'
                            + '#SYSTEMATICSDIR#/' + meNameNumEventsPassedAHtoMuTau
                         )
                    )
                ),
                AHtoElecTau = cms.PSet(
                    template = cms.string(
                        dqmDirectoryTemplateAHtoElecTau % 'WplusJetsSum'
                       + '#SYSTEMATICSDIR#/' + meNameTemplateAHtoElecTau
                    ),
                    systematics = cms.vstring(AHtoElecTau_systematics),
                    normalization = cms.PSet(
                         numEventsProcessed = cms.string(
                             dqmDirectoryFilterStatAHtoElecTau % 'WplusJetsSum'
                            + '#SYSTEMATICSDIR#/' + meNameNumEventsProcessedAHtoElecTau
                         ),
                         numEventsPassed = cms.string(
                             dqmDirectoryFilterStatAHtoElecTau % 'WplusJetsSum'
                            + '#SYSTEMATICSDIR#/' + meNameNumEventsPassedAHtoElecTau
                         )
                    )
                )
            ),
            outputFilePath = cms.string(""),
	    outputFileName = cms.string("wjets_#CHANNEL_OUTPUTFILENAME#.hst")
        ),
        ##TTplusJets = cms.PSet(
        ##    distributions = cms.PSet(
        ##        AHtoMuTau = cms.PSet(
        ##            template = cms.string(
        ##                dqmDirectoryTemplateAHtoMuTau % 'TTplusJets'
        ##               + '#SYSTEMATICSDIR#/' + meNameTemplateAHtoMuTau
        ##            ),
        ##            systematics = cms.vstring(AHtoMuTau_systematics),
        ##            normalization = cms.PSet(
        ##                 numEventsProcessed = cms.string(
        ##                     dqmDirectoryFilterStatAHtoMuTau % 'TTplusJets'
        ##                    + '#SYSTEMATICSDIR#/' + meNameNumEventsProcessedAHtoMuTau
        ##                 ),
        ##                 numEventsPassed = cms.string(
        ##                     dqmDirectoryFilterStatAHtoMuTau % 'TTplusJets'
        ##                    + '#SYSTEMATICSDIR#/' + meNameNumEventsPassedAHtoMuTau
        ##                 )
        ##            )
        ##        )
        ##    ),
        ##    outputFilePath = cms.string(""),
	##    outputFileName = cms.string("ttbar_#CHANNEL_OUTPUTFILENAME#.hst")
        ##),
        gammaPlusJetsSum = cms.PSet(
            distributions = cms.PSet(
                AHtoElecTau = cms.PSet(
                    template = cms.string(
                        dqmDirectoryTemplateAHtoElecTau % 'gammaPlusJetsSum'
                       + '#SYSTEMATICSDIR#/' + meNameTemplateAHtoElecTau
                    ),
                    systematics = cms.vstring(AHtoElecTau_systematics),
                    normalization = cms.PSet(
                         numEventsProcessed = cms.string(
                             dqmDirectoryFilterStatAHtoElecTau % 'gammaPlusJetsSum'
                            + '#SYSTEMATICSDIR#/' + meNameNumEventsProcessedAHtoElecTau
                         ),
                         numEventsPassed = cms.string(
                             dqmDirectoryFilterStatAHtoElecTau % 'gammaPlusJetsSum'
                            + '#SYSTEMATICSDIR#/' + meNameNumEventsPassedAHtoElecTau
                         )
                    )
                )
            ),
            outputFilePath = cms.string(""),
	    outputFileName = cms.string("gammajets_#CHANNEL_OUTPUTFILENAME#.hst")
        ),
        data = cms.PSet(
            distributions = cms.PSet(
                AHtoMuTau = cms.PSet(
                    template = cms.string(
                        dqmDirectoryTemplateAHtoMuTau % 'data'
                       + '#SYSTEMATICSDIR#/' + meNameTemplateAHtoMuTau
                    ),
                    systematics = cms.vstring(AHtoMuTau_systematics),
                    normalization = cms.PSet(
                         numEventsProcessed = cms.string(
                             dqmDirectoryFilterStatAHtoMuTau % 'data'
                            + '#SYSTEMATICSDIR#/' + meNameNumEventsProcessedAHtoMuTau
                         ),
                         numEventsPassed = cms.string(
                             dqmDirectoryFilterStatAHtoMuTau % 'data'
                            + '#SYSTEMATICSDIR#/' + meNameNumEventsPassedAHtoMuTau
                         )
                    )
                ),
                AHtoElecTau = cms.PSet(
                    template = cms.string(
                        dqmDirectoryTemplateAHtoElecTau % 'Data'
                       + '#SYSTEMATICSDIR#/' + meNameTemplateAHtoElecTau
                    ),
                    systematics = cms.vstring(AHtoElecTau_systematics),
                    normalization = cms.PSet(
                         numEventsProcessed = cms.string(
                             dqmDirectoryFilterStatAHtoElecTau % 'Data'
                            + '#SYSTEMATICSDIR#/' + meNameNumEventsProcessedAHtoElecTau
                         ),
                         numEventsPassed = cms.string(
                             dqmDirectoryFilterStatAHtoElecTau % 'Data'
                            + '#SYSTEMATICSDIR#/' + meNameNumEventsPassedAHtoElecTau
                         )
                    )
                )
            ),
            outputFilePath = cms.string(""),
	    outputFileName = cms.string("data_#CHANNEL_OUTPUTFILENAME#.hst")
        )
    )

    ##systematics = cms.PSet(
    ##	  elecEnUp = cms.PSet(
    ##	      dqmDirectory = cms.string('sysUncertaintyHistManagerResults/sysElecEnUp'),
    ## 	      outputFilePath = cms.string("mu_pt+1")
    ##    ),
    ##	  elecEnDown = cms.PSet(
    ##	      dqmDirectory = cms.string('sysUncertaintyHistManagerResults/sysElecEnDown'),
    ##	      outputFilePath = cms.string("mu_pt-1")
    ##    ),
    ##	  muonPtUp = cms.PSet(
    ##	      dqmDirectory = cms.string('sysUncertaintyHistManagerResults/sysMuonPtUp'),
    ## 	      outputFilePath = cms.string("mu_pt+1")
    ##    ),
    ##	  muonPtDown = cms.PSet(
    ##	      dqmDirectory = cms.string('sysUncertaintyHistManagerResults/sysMuonPtDown'),
    ##	      outputFilePath = cms.string("mu_pt-1")
    ##    ),                                                  
    ##	  tauJetEnUp = cms.PSet(
    ##	      dqmDirectory = cms.string('sysUncertaintyHistManagerResults/sysTauJetEnUp'),
    ## 	      outputFilePath = cms.string("tau_es+1")
    ##    ),
    ##	  tauJetEnDown = cms.PSet(
    ##	      dqmDirectory = cms.string('sysUncertaintyHistManagerResults/sysTauJetEnDown'),
    ##	      outputFilePath = cms.string("tau_es-1")
    ##    ),
    ##	  jetEnUp = cms.PSet(
    ##	      dqmDirectory = cms.string('sysUncertaintyHistManagerResults/sysJetEnUp'),
    ## 	      outputFilePath = cms.string("jet_es+1")
    ##    ),
    ##	  jetEnDown = cms.PSet(
    ##	      dqmDirectory = cms.string('sysUncertaintyHistManagerResults/sysJetEnDown'),
    ##	      outputFilePath = cms.string("jet_es-1")
    ##    )                                                
    ##)
)

for higgsMassPoint in higgsMassPoints:

    pset = cms.PSet(
        distributions = cms.PSet(
            AHtoMuTau = cms.PSet(
                template = cms.string(
                    dqmDirectoryTemplateAHtoMuTau % ('A%sSum' % higgsMassPoint)
                   + '#SYSTEMATICSDIR#/' + meNameTemplateAHtoMuTau
                ),
                systematics = cms.vstring(AHtoMuTau_systematics),
                normalization = cms.PSet(
                    numEventsProcessed = cms.string(
                        dqmDirectoryFilterStatAHtoMuTau % ('A%sSum' % higgsMassPoint)
                       + '#SYSTEMATICSDIR#/' + meNameNumEventsProcessedAHtoMuTau
                    ),
                    numEventsPassed = cms.string(
                        dqmDirectoryFilterStatAHtoMuTau % ('A%sSum' % higgsMassPoint)
                       + '#SYSTEMATICSDIR#/' + meNameNumEventsPassedAHtoMuTau
                    )
                )
            ),
            AHtoElecTau = cms.PSet(
                template = cms.string(
                    dqmDirectoryTemplateAHtoMuTau % ('A%sSum' % higgsMassPoint)
                   + '#SYSTEMATICSDIR#/' + meNameTemplateAHtoMuTau
                ),
                systematics = cms.vstring(),
                normalization = cms.PSet(
                    numEventsProcessed = cms.string(
                        dqmDirectoryFilterStatAHtoMuTau % ('A%sSum' % higgsMassPoint)
                       + '#SYSTEMATICSDIR#/' + meNameNumEventsProcessedAHtoMuTau
                    ),
                    numEventsPassed = cms.string(
                        ('/export/harvested/A%sSum/ahElecTauAnalyzer_prediction/FilterStatistics/' \
                       + '#SYSTEMATICSDIR#/evtSelElecTauPairZeeHypothesisVeto/passed_cumulative_numWeighted#a1#s1') % higgsMassPoint
                    )
                )
            )
        ),
        outputFilePath = cms.string("m%s" % higgsMassPoint),
        outputFileName = cms.string("A_#CHANNEL_OUTPUTFILENAME#.hst")
    )
    
    setattr(process.exportAnalysisResults.processes, "A%s" % higgsMassPoint, pset)

print("computing AHtoMuTau effectice cross-sections...")

numeratorAHtoMuTau = 'FilterStatistics/evtSelNonCentralJetEt20bTag/passed_cumulative_numWeighted#a1#s1'
denominatorAHtoMuTau = 'FilterStatistics/genPhaseSpaceCut/passed_cumulative_numWeighted#a1#s1'
numEventsPassedAHtoMuTau = 'FilterStatistics/evtSelNonCentralJetEt20bTag/passed_cumulative_numWeighted#a1#s1'
processEntryAHtoMuTau = cms.PSet(
    efficiency = cms.PSet(
        numerator = cms.string(numeratorAHtoMuTau),
        denominator = cms.string(denominatorAHtoMuTau)
    ),
    numEventsPassed = cms.string(numEventsPassedAHtoMuTau),
    dqmDirectory = cms.string('')
)

process.compDQMEffXsecAHtoMuTau = cms.EDAnalyzer("DQMEffXsecCalculator",
    dataIntLumi = cms.double(ZtoMuTau.TARGET_LUMI),
    channels = cms.PSet(
        Ztautau = processEntryAHtoMuTau.clone(
            dqmDirectory = cms.string('/export/harvested/Ztautau/ahMuTauAnalyzer_woBtag')
        ),
        Zmumu = processEntryAHtoMuTau.clone(
            dqmDirectory = cms.string('/export/harvested/Zmumu/ahMuTauAnalyzer_woBtag')
        ),
        QCD = processEntryAHtoMuTau.clone(
            dqmDirectory = cms.string('/export/harvested/qcdSum/ahMuTauAnalyzer_woBtag')
        ),
        WplusJets = processEntryAHtoMuTau.clone(
            dqmDirectory = cms.string('/export/harvested/WplusJets/ahMuTauAnalyzer_woBtag')
        ##),
        ##TTplusJets = processEntryAHtoMuTau.clone(
        ##    dqmDirectory = cms.string('/export/harvested/TTplusJets/ahMuTauAnalyzer_woBtag')
        )
    )
)

print("computing AHtoElecTau effectice cross-sections...")

numeratorAHtoElecTau = 'FilterStatistics/evtSelElecTauPairZeeHypothesisVeto/passed_cumulative_numWeighted#a1#s1'
denominatorAHtoElecTau = 'FilterStatistics/genPhaseSpaceCut/passed_cumulative_numWeighted#a1#s1'
numEventsPassedAHtoElecTau = 'FilterStatistics/evtSelElecTauPairZeeHypothesisVeto/passed_cumulative_numWeighted#a1#s1'
processEntryAHtoElecTau = cms.PSet(
    efficiency = cms.PSet(
        numerator = cms.string(numeratorAHtoElecTau),
        denominator = cms.string(denominatorAHtoElecTau)
    ),
    numEventsPassed = cms.string(numEventsPassedAHtoElecTau),
    dqmDirectory = cms.string('')
)

process.compDQMEffXsecAHtoElecTau = cms.EDAnalyzer("DQMEffXsecCalculator",
    dataIntLumi = cms.double(32.0),
    channels = cms.PSet(
        Ztautau = processEntryAHtoElecTau.clone(
            dqmDirectory = cms.string('/export/summed/harvested/Ztautau/zElecTauAnalyzer')
        ),
        Zee = processEntryAHtoElecTau.clone(
            dqmDirectory = cms.string('/export/summed/harvested/Zee/zElecTauAnalyzer')
        ),
        QCD = processEntryAHtoElecTau.clone(
            dqmDirectory = cms.string('/export/summed/harvested/qcdSum/zElecTauAnalyzer')
        ),
        WplusJets = processEntryAHtoElecTau.clone(
            dqmDirectory = cms.string('/export/summed/harvested/WplusJetsSum/zElecTauAnalyzer')
        ),
        ##TTplusJets = processEntryAHtoElecTau.clone(
        ##    dqmDirectory = cms.string('/export/summed/harvested/TTplusJets/zElecTauAnalyzer')
        ##),
        gammaPlusJets = processEntryAHtoElecTau.clone(
            dqmDirectory = cms.string('/export/summed/harvested/gammaPlusJetsSum/zElecTauAnalyzer')
        )
    )
)

process.p = cms.Path(
    process.loadAnalysisResults
   + process.sumAHtoElecTau
   + process.compAHtoElecTauPrediction
   + process.dumpDQMStore 
   + process.exportAnalysisResults
   + process.compDQMEffXsecAHtoMuTau 
   + process.compDQMEffXsecAHtoElecTau
)

# print-out all python configuration parameter information
print process.dumpPython()