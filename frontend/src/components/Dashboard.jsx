import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { 
  Plus, 
  FileText, 
  TrendingUp, 
  Calculator, 
  Clock, 
  CheckCircle, 
  AlertCircle,
  Building,
  Euro,
  Calendar,
  ArrowRight,
  Sparkles
} from 'lucide-react'

export default function Dashboard({ user }) {
  const navigate = useNavigate()
  const [declarations, setDeclarations] = useState([])
  const [stats, setStats] = useState({
    totalBiens: 0,
    recettesAnnuelles: 0,
    economiesFiscales: 0,
    declarationsCompletes: 0
  })

  useEffect(() => {
    // Simulation de chargement des données
    const loadData = () => {
      const mockDeclarations = [
        {
          id: 1,
          annee: 2024,
          statut: 'en_cours',
          progression: 65,
          biens: 2,
          recettes: 24000,
          resultat: 3200,
          dateModification: '2024-07-20'
        },
        {
          id: 2,
          annee: 2023,
          statut: 'complete',
          progression: 100,
          biens: 1,
          recettes: 18000,
          resultat: 2100,
          dateModification: '2024-03-15',
          teletransmise: true
        }
      ]
      
      setDeclarations(mockDeclarations)
      
      // Calcul des statistiques
      const totalBiens = mockDeclarations.reduce((sum, d) => sum + d.biens, 0)
      const recettesAnnuelles = mockDeclarations
        .filter(d => d.annee === 2024)
        .reduce((sum, d) => sum + d.recettes, 0)
      const economiesFiscales = 8500 // Estimation
      const declarationsCompletes = mockDeclarations.filter(d => d.statut === 'complete').length
      
      setStats({
        totalBiens,
        recettesAnnuelles,
        economiesFiscales,
        declarationsCompletes
      })
    }
    
    setTimeout(loadData, 300)
  }, [])

  const getStatutBadge = (statut, teletransmise = false) => {
    if (teletransmise) {
      return <Badge className="bg-green-100 text-green-800 border-green-200">Télétransmise</Badge>
    }
    
    switch (statut) {
      case 'complete':
        return <Badge className="bg-blue-100 text-blue-800 border-blue-200">Complète</Badge>
      case 'en_cours':
        return <Badge className="bg-yellow-100 text-yellow-800 border-yellow-200">En cours</Badge>
      case 'brouillon':
        return <Badge variant="outline">Brouillon</Badge>
      default:
        return <Badge variant="outline">Nouvelle</Badge>
    }
  }

  const getStatutIcon = (statut, teletransmise = false) => {
    if (teletransmise) {
      return <CheckCircle className="h-5 w-5 text-green-600" />
    }
    
    switch (statut) {
      case 'complete':
        return <CheckCircle className="h-5 w-5 text-blue-600" />
      case 'en_cours':
        return <Clock className="h-5 w-5 text-yellow-600" />
      default:
        return <AlertCircle className="h-5 w-5 text-gray-400" />
    }
  }

  return (
    <div className="space-y-8">
      {/* En-tête avec salutation */}
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Bonjour {user.firstName} ! 👋
        </h1>
        <p className="text-lg text-gray-600">
          Gérez vos déclarations LMNP en toute simplicité
        </p>
      </div>

      {/* Statistiques rapides */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card className="bg-gradient-to-br from-blue-50 to-blue-100 border-blue-200">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-blue-600">Biens LMNP</p>
                <p className="text-3xl font-bold text-blue-900">{stats.totalBiens}</p>
              </div>
              <Building className="h-8 w-8 text-blue-600" />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-green-50 to-green-100 border-green-200">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-green-600">Recettes 2024</p>
                <p className="text-3xl font-bold text-green-900">
                  {stats.recettesAnnuelles.toLocaleString()}€
                </p>
              </div>
              <Euro className="h-8 w-8 text-green-600" />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-purple-50 to-purple-100 border-purple-200">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-purple-600">Économies fiscales</p>
                <p className="text-3xl font-bold text-purple-900">
                  {stats.economiesFiscales.toLocaleString()}€
                </p>
              </div>
              <TrendingUp className="h-8 w-8 text-purple-600" />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-orange-50 to-orange-100 border-orange-200">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-orange-600">Déclarations</p>
                <p className="text-3xl font-bold text-orange-900">{stats.declarationsCompletes}</p>
              </div>
              <FileText className="h-8 w-8 text-orange-600" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Actions rapides */}
      <Card className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white">
        <CardContent className="p-8">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-2xl font-bold mb-2">Nouvelle déclaration 2024</h3>
              <p className="text-blue-100 mb-4">
                Créez votre déclaration LMNP en 30 minutes avec l'assistance IA
              </p>
              <div className="flex items-center space-x-2 text-blue-100">
                <Sparkles className="h-4 w-4" />
                <span className="text-sm">Calculs automatiques • Optimisation fiscale • Conformité garantie</span>
              </div>
            </div>
            <Button 
              size="lg" 
              className="bg-white text-blue-600 hover:bg-blue-50"
              onClick={() => navigate('/nouvelle-declaration')}
            >
              <Plus className="h-5 w-5 mr-2" />
              Commencer
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Liste des déclarations */}
      <div>
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-gray-900">Mes déclarations</h2>
          <Button variant="outline" onClick={() => navigate('/nouvelle-declaration')}>
            <Plus className="h-4 w-4 mr-2" />
            Nouvelle déclaration
          </Button>
        </div>

        <div className="grid gap-6">
          {declarations.map((declaration) => (
            <Card key={declaration.id} className="hover:shadow-lg transition-shadow cursor-pointer">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    {getStatutIcon(declaration.statut, declaration.teletransmise)}
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900">
                        Déclaration {declaration.annee}
                      </h3>
                      <p className="text-gray-600">
                        {declaration.biens} bien{declaration.biens > 1 ? 's' : ''} • 
                        {declaration.recettes.toLocaleString()}€ de recettes
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center space-x-4">
                    {getStatutBadge(declaration.statut, declaration.teletransmise)}
                    
                    {declaration.statut === 'en_cours' && (
                      <div className="text-right">
                        <p className="text-sm text-gray-600 mb-1">Progression</p>
                        <div className="flex items-center space-x-2">
                          <Progress value={declaration.progression} className="w-24" />
                          <span className="text-sm font-medium">{declaration.progression}%</span>
                        </div>
                      </div>
                    )}

                    <Button 
                      variant="outline"
                      onClick={() => navigate(`/declaration/${declaration.id}`)}
                    >
                      {declaration.statut === 'en_cours' ? 'Continuer' : 'Voir'}
                      <ArrowRight className="h-4 w-4 ml-2" />
                    </Button>
                  </div>
                </div>

                {declaration.statut === 'complete' && (
                  <div className="mt-4 p-4 bg-gray-50 rounded-lg">
                    <div className="grid grid-cols-3 gap-4 text-center">
                      <div>
                        <p className="text-sm text-gray-600">Résultat fiscal</p>
                        <p className="text-lg font-semibold text-gray-900">
                          {declaration.resultat.toLocaleString()}€
                        </p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600">Dernière modification</p>
                        <p className="text-lg font-semibold text-gray-900">
                          {new Date(declaration.dateModification).toLocaleDateString('fr-FR')}
                        </p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600">Statut</p>
                        <p className="text-lg font-semibold text-gray-900">
                          {declaration.teletransmise ? 'Télétransmise' : 'Prête'}
                        </p>
                      </div>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          ))}

          {declarations.length === 0 && (
            <Card className="text-center py-12">
              <CardContent>
                <FileText className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  Aucune déclaration
                </h3>
                <p className="text-gray-600 mb-6">
                  Commencez votre première déclaration LMNP dès maintenant
                </p>
                <Button onClick={() => navigate('/nouvelle-declaration')}>
                  <Plus className="h-4 w-4 mr-2" />
                  Créer ma première déclaration
                </Button>
              </CardContent>
            </Card>
          )}
        </div>
      </div>

      {/* Conseils et aide */}
      <Card className="bg-gradient-to-r from-green-50 to-blue-50 border-green-200">
        <CardContent className="p-6">
          <div className="flex items-start space-x-4">
            <div className="bg-green-100 p-2 rounded-lg">
              <Sparkles className="h-6 w-6 text-green-600" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Conseils personnalisés
              </h3>
              <p className="text-gray-600 mb-4">
                Basé sur vos données, voici nos recommandations pour optimiser votre fiscalité LMNP :
              </p>
              <ul className="space-y-2 text-sm text-gray-700">
                <li className="flex items-center space-x-2">
                  <CheckCircle className="h-4 w-4 text-green-600" />
                  <span>Vous êtes éligible au régime micro-BIC avec 50% d'abattement</span>
                </li>
                <li className="flex items-center space-x-2">
                  <CheckCircle className="h-4 w-4 text-green-600" />
                  <span>Pensez à déduire vos frais de gestion locative</span>
                </li>
                <li className="flex items-center space-x-2">
                  <CheckCircle className="h-4 w-4 text-green-600" />
                  <span>Optimisation possible avec le régime réel (+1 200€ d'économies)</span>
                </li>
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

