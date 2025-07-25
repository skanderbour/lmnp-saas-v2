import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { 
  ArrowLeft, 
  ArrowRight, 
  Building, 
  Euro, 
  Calculator, 
  FileText, 
  Send,
  CheckCircle,
  Sparkles
} from 'lucide-react'

// Étapes du wizard
const ETAPES = [
  { id: 'biens', titre: 'Biens immobiliers', icon: Building, description: 'Ajoutez vos biens LMNP' },
  { id: 'recettes', titre: 'Recettes', icon: Euro, description: 'Saisissez vos loyers et autres recettes' },
  { id: 'depenses', titre: 'Dépenses', icon: FileText, description: 'Déclarez vos charges déductibles' },
  { id: 'amortissements', titre: 'Amortissements', icon: Calculator, description: 'Calculs automatiques' },
  { id: 'recapitulatif', titre: 'Récapitulatif', icon: CheckCircle, description: 'Validation et télétransmission' }
]

export default function DeclarationWizard({ user, isNew = false }) {
  const { id } = useParams()
  const navigate = useNavigate()
  const [etapeActuelle, setEtapeActuelle] = useState(0)
  const [declaration, setDeclaration] = useState({
    id: isNew ? null : parseInt(id),
    annee: 2024,
    statut: 'en_cours',
    biens: [],
    progression: 0
  })

  useEffect(() => {
    if (!isNew && id) {
      // Charger la déclaration existante
      // Simulation de chargement
      setTimeout(() => {
        setDeclaration(prev => ({
          ...prev,
          progression: 65,
          biens: [
            {
              id: 1,
              adresse: '123 Rue de la Paix, 75001 Paris',
              recettes: 24000,
              depenses: 8500,
              amortissements: 7200
            }
          ]
        }))
        setEtapeActuelle(2) // Reprendre à l'étape des dépenses
      }, 500)
    }
  }, [id, isNew])

  const progression = ((etapeActuelle + 1) / ETAPES.length) * 100

  const allerEtapeSuivante = () => {
    if (etapeActuelle < ETAPES.length - 1) {
      setEtapeActuelle(etapeActuelle + 1)
      setDeclaration(prev => ({
        ...prev,
        progression: Math.max(prev.progression, ((etapeActuelle + 2) / ETAPES.length) * 100)
      }))
    }
  }

  const allerEtapePrecedente = () => {
    if (etapeActuelle > 0) {
      setEtapeActuelle(etapeActuelle - 1)
    }
  }

  const retourDashboard = () => {
    navigate('/')
  }

  const renderEtapeContent = () => {
    const etape = ETAPES[etapeActuelle]
    
    switch (etape.id) {
      case 'biens':
        return <EtapeBiens declaration={declaration} setDeclaration={setDeclaration} />
      case 'recettes':
        return <EtapeRecettes declaration={declaration} setDeclaration={setDeclaration} />
      case 'depenses':
        return <EtapeDepenses declaration={declaration} setDeclaration={setDeclaration} />
      case 'amortissements':
        return <EtapeAmortissements declaration={declaration} setDeclaration={setDeclaration} />
      case 'recapitulatif':
        return <EtapeRecapitulatif declaration={declaration} setDeclaration={setDeclaration} />
      default:
        return <div>Étape non trouvée</div>
    }
  }

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* En-tête */}
      <div className="flex items-center justify-between">
        <Button variant="outline" onClick={retourDashboard}>
          <ArrowLeft className="h-4 w-4 mr-2" />
          Retour au tableau de bord
        </Button>
        
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900">
            Déclaration LMNP {declaration.annee}
          </h1>
          <p className="text-gray-600">
            {isNew ? 'Nouvelle déclaration' : `Déclaration #${declaration.id}`}
          </p>
        </div>
        
        <Badge className="bg-blue-100 text-blue-800">
          {Math.round(progression)}% complété
        </Badge>
      </div>

      {/* Barre de progression */}
      <Card>
        <CardContent className="p-6">
          <div className="mb-4">
            <div className="flex justify-between items-center mb-2">
              <span className="text-sm font-medium text-gray-700">Progression</span>
              <span className="text-sm text-gray-500">{Math.round(progression)}%</span>
            </div>
            <Progress value={progression} className="h-2" />
          </div>
          
          {/* Navigation des étapes */}
          <div className="flex justify-between">
            {ETAPES.map((etape, index) => {
              const Icon = etape.icon
              const isActive = index === etapeActuelle
              const isCompleted = index < etapeActuelle || progression >= ((index + 1) / ETAPES.length) * 100
              
              return (
                <div
                  key={etape.id}
                  className={`flex flex-col items-center space-y-2 cursor-pointer transition-colors ${
                    isActive ? 'text-blue-600' : isCompleted ? 'text-green-600' : 'text-gray-400'
                  }`}
                  onClick={() => setEtapeActuelle(index)}
                >
                  <div className={`p-3 rounded-full ${
                    isActive ? 'bg-blue-100' : isCompleted ? 'bg-green-100' : 'bg-gray-100'
                  }`}>
                    <Icon className="h-5 w-5" />
                  </div>
                  <div className="text-center">
                    <p className="text-sm font-medium">{etape.titre}</p>
                    <p className="text-xs text-gray-500">{etape.description}</p>
                  </div>
                </div>
              )
            })}
          </div>
        </CardContent>
      </Card>

      {/* Contenu de l'étape */}
      <div className="min-h-[500px]">
        {renderEtapeContent()}
      </div>

      {/* Navigation */}
      <Card>
        <CardContent className="p-6">
          <div className="flex justify-between items-center">
            <Button
              variant="outline"
              onClick={allerEtapePrecedente}
              disabled={etapeActuelle === 0}
            >
              <ArrowLeft className="h-4 w-4 mr-2" />
              Précédent
            </Button>
            
            <div className="text-center">
              <p className="text-sm text-gray-600">
                Étape {etapeActuelle + 1} sur {ETAPES.length}
              </p>
            </div>
            
            <Button
              onClick={allerEtapeSuivante}
              disabled={etapeActuelle === ETAPES.length - 1}
              className="bg-blue-600 hover:bg-blue-700"
            >
              Suivant
              <ArrowRight className="h-4 w-4 ml-2" />
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

// Composants pour chaque étape
function EtapeBiens({ declaration, setDeclaration }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <Building className="h-5 w-5" />
          <span>Vos biens immobiliers LMNP</span>
        </CardTitle>
        <CardDescription>
          Ajoutez tous vos biens en location meublée non professionnelle
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="text-center py-12 border-2 border-dashed border-gray-300 rounded-lg">
          <Building className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            Aucun bien ajouté
          </h3>
          <p className="text-gray-600 mb-6">
            Commencez par ajouter votre premier bien immobilier
          </p>
          <Button className="bg-blue-600 hover:bg-blue-700">
            <Building className="h-4 w-4 mr-2" />
            Ajouter un bien
          </Button>
        </div>
        
        <div className="bg-blue-50 p-4 rounded-lg">
          <div className="flex items-start space-x-3">
            <Sparkles className="h-5 w-5 text-blue-600 mt-0.5" />
            <div>
              <h4 className="font-semibold text-blue-900">Calculs automatiques</h4>
              <p className="text-blue-700 text-sm">
                L'IA calculera automatiquement la répartition terrain/construction et les amortissements selon votre localisation.
              </p>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

function EtapeRecettes({ declaration, setDeclaration }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <Euro className="h-5 w-5" />
          <span>Recettes et loyers</span>
        </CardTitle>
        <CardDescription>
          Saisissez vos loyers et autres recettes de l'année
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="text-center py-12">
          <Euro className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-600">
            Fonctionnalité en cours de développement
          </p>
        </div>
      </CardContent>
    </Card>
  )
}

function EtapeDepenses({ declaration, setDeclaration }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <FileText className="h-5 w-5" />
          <span>Dépenses déductibles</span>
        </CardTitle>
        <CardDescription>
          Déclarez toutes vos charges déductibles
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="text-center py-12">
          <FileText className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-600">
            Fonctionnalité en cours de développement
          </p>
        </div>
      </CardContent>
    </Card>
  )
}

function EtapeAmortissements({ declaration, setDeclaration }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <Calculator className="h-5 w-5" />
          <span>Amortissements</span>
        </CardTitle>
        <CardDescription>
          Calculs automatiques selon la réglementation fiscale
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="text-center py-12">
          <Calculator className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-600">
            Fonctionnalité en cours de développement
          </p>
        </div>
      </CardContent>
    </Card>
  )
}

function EtapeRecapitulatif({ declaration, setDeclaration }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <CheckCircle className="h-5 w-5" />
          <span>Récapitulatif et télétransmission</span>
        </CardTitle>
        <CardDescription>
          Vérifiez vos données et télétransmettez votre déclaration
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="text-center py-12">
          <Send className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-600">
            Fonctionnalité en cours de développement
          </p>
        </div>
      </CardContent>
    </Card>
  )
}

