import { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Calculator, Shield, Zap, TrendingUp } from 'lucide-react'

export default function LoginPage({ onLogin }) {
  const [isLogin, setIsLogin] = useState(true)
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    firstName: '',
    lastName: '',
    acceptTerms: false
  })
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    
    // Simulation d'authentification
    setTimeout(() => {
      const userData = {
        id: 1,
        email: formData.email,
        firstName: formData.firstName || 'Utilisateur',
        lastName: formData.lastName || 'Demo',
        isExpert: formData.email.includes('expert') || formData.email.includes('comptable')
      }
      
      onLogin(userData)
      setLoading(false)
    }, 1000)
  }

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 flex items-center justify-center p-4">
      <div className="w-full max-w-6xl grid lg:grid-cols-2 gap-8 items-center">
        
        {/* Section gauche - Présentation */}
        <div className="space-y-8">
          <div className="text-center lg:text-left">
            <div className="flex items-center justify-center lg:justify-start space-x-3 mb-6">
              <div className="bg-blue-600 p-3 rounded-xl">
                <Calculator className="h-8 w-8 text-white" />
              </div>
              <div>
                <h1 className="text-3xl font-bold text-gray-900">LMNP Expert</h1>
                <p className="text-gray-600">Déclarations fiscales simplifiées</p>
              </div>
            </div>
            
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Votre déclaration LMNP en 
              <span className="text-blue-600"> 30 minutes</span>
            </h2>
            <p className="text-xl text-gray-600 mb-8">
              L'IA calcule tout automatiquement. Vous n'avez qu'à saisir vos données.
            </p>
          </div>

          {/* Avantages */}
          <div className="grid gap-6">
            <div className="flex items-start space-x-4">
              <div className="bg-green-100 p-2 rounded-lg">
                <Zap className="h-6 w-6 text-green-600" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900">Calculs automatiques</h3>
                <p className="text-gray-600">Amortissements, optimisations fiscales, tout est calculé pour vous</p>
              </div>
            </div>
            
            <div className="flex items-start space-x-4">
              <div className="bg-blue-100 p-2 rounded-lg">
                <Shield className="h-6 w-6 text-blue-600" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900">Conformité garantie</h3>
                <p className="text-gray-600">Règles fiscales 2024-2025 intégrées et mises à jour automatiquement</p>
              </div>
            </div>
            
            <div className="flex items-start space-x-4">
              <div className="bg-purple-100 p-2 rounded-lg">
                <TrendingUp className="h-6 w-6 text-purple-600" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900">Optimisation intelligente</h3>
                <p className="text-gray-600">Micro-BIC vs régime réel : l'IA choisit le plus avantageux</p>
              </div>
            </div>
          </div>
        </div>

        {/* Section droite - Formulaire */}
        <div className="w-full max-w-md mx-auto">
          <Card className="shadow-xl border-0">
            <CardHeader className="text-center">
              <CardTitle className="text-2xl">
                {isLogin ? 'Connexion' : 'Créer un compte'}
              </CardTitle>
              <CardDescription>
                {isLogin 
                  ? 'Accédez à vos déclarations LMNP' 
                  : 'Commencez votre première déclaration'
                }
              </CardDescription>
            </CardHeader>
            
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-4">
                {!isLogin && (
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="firstName">Prénom</Label>
                      <Input
                        id="firstName"
                        name="firstName"
                        value={formData.firstName}
                        onChange={handleInputChange}
                        required={!isLogin}
                        placeholder="Jean"
                      />
                    </div>
                    <div>
                      <Label htmlFor="lastName">Nom</Label>
                      <Input
                        id="lastName"
                        name="lastName"
                        value={formData.lastName}
                        onChange={handleInputChange}
                        required={!isLogin}
                        placeholder="Dupont"
                      />
                    </div>
                  </div>
                )}
                
                <div>
                  <Label htmlFor="email">Email</Label>
                  <Input
                    id="email"
                    name="email"
                    type="email"
                    value={formData.email}
                    onChange={handleInputChange}
                    required
                    placeholder="jean.dupont@email.com"
                  />
                </div>
                
                <div>
                  <Label htmlFor="password">Mot de passe</Label>
                  <Input
                    id="password"
                    name="password"
                    type="password"
                    value={formData.password}
                    onChange={handleInputChange}
                    required
                    placeholder="••••••••"
                  />
                </div>
                
                {!isLogin && (
                  <div className="flex items-center space-x-2">
                    <input
                      id="acceptTerms"
                      name="acceptTerms"
                      type="checkbox"
                      checked={formData.acceptTerms}
                      onChange={handleInputChange}
                      required={!isLogin}
                      className="rounded border-gray-300"
                    />
                    <Label htmlFor="acceptTerms" className="text-sm">
                      J'accepte les conditions d'utilisation
                    </Label>
                  </div>
                )}
                
                <Button 
                  type="submit" 
                  className="w-full bg-blue-600 hover:bg-blue-700"
                  disabled={loading}
                >
                  {loading ? (
                    <div className="flex items-center space-x-2">
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                      <span>Connexion...</span>
                    </div>
                  ) : (
                    isLogin ? 'Se connecter' : 'Créer mon compte'
                  )}
                </Button>
              </form>
              
              <div className="mt-6 text-center">
                <button
                  type="button"
                  onClick={() => setIsLogin(!isLogin)}
                  className="text-blue-600 hover:text-blue-700 text-sm"
                >
                  {isLogin 
                    ? "Pas encore de compte ? Créer un compte" 
                    : "Déjà un compte ? Se connecter"
                  }
                </button>
              </div>
              
              {/* Demo rapide */}
              <div className="mt-6 p-4 bg-gray-50 rounded-lg">
                <p className="text-sm text-gray-600 text-center mb-2">
                  <strong>Demo rapide :</strong> Utilisez n'importe quel email/mot de passe
                </p>
                <Button
                  type="button"
                  variant="outline"
                  className="w-full"
                  onClick={() => {
                    setFormData({
                      email: 'demo@lmnp-expert.fr',
                      password: 'demo123',
                      firstName: 'Utilisateur',
                      lastName: 'Demo',
                      acceptTerms: true
                    })
                  }}
                >
                  Remplir avec données de demo
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}

